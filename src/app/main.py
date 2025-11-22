#!/usr/bin/env python3
"""
Main entry point for the Project Management Dashboard application.
This script aggregates data from project sheets into a management sheet.
"""

import os
import time
import logging
import hashlib
from typing import Dict, List, Any

import gspread

from src.utils import load_credentials
from .config import Config
from .sheets_utils import find_column_index, ensure_worksheet_exists

import os

# Set up logging with level configurable via environment variable
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProjectDashboard:
    def __init__(self, update_interval: int = None):
        """
        Initialize the Project Dashboard.

        Args:
            update_interval: Interval in seconds between updates (defaults to config value)
        """
        self.update_interval = update_interval or Config.UPDATE_INTERVAL
        self.gc = None
        self.spreadsheet = None
        self.management_sheet_name = Config.MANAGEMENT_SHEET_NAME
        self.previous_data_hash = None
        
    def initialize_connection(self):
        """Initialize connection to Google Sheets."""
        load_credentials()
        self.gc = gspread.service_account(filename=os.getenv("CREDENTIALS"))
        self.spreadsheet = self.gc.open_by_key(os.getenv("GOOGLE_SHEET_ID"))
        logger.info("Connected to Google Sheets API")
        
    def get_worksheet_by_name(self, name: str):
        """Get a worksheet by name, creating it if it doesn't exist."""
        # Using utility function that handles worksheet creation
        return ensure_worksheet_exists(self.spreadsheet, name)
    
    def get_project_sheets(self) -> List:
        """Get all project sheets (excluding the management sheet)."""
        all_worksheets = self.spreadsheet.worksheets()
        project_sheets = []
        
        for worksheet in all_worksheets:
            if worksheet.title != self.management_sheet_name:
                project_sheets.append(worksheet)
                
        return project_sheets
    
    def clear_management_sheet(self, management_sheet):
        """Clear all rows except the header in the management sheet."""
        # For management sheet, we know it has 10 columns, so we'll clear using the exact range
        all_values = management_sheet.get_all_values()

        if len(all_values) >= 2:
            # Calculate how many rows to clear (from row 2 to the last row)
            last_row = len(all_values)
            num_rows_to_clear = last_row - 2 + 1  # from row 2 to last row

            if num_rows_to_clear > 0:
                # Create empty rows for 10 columns ('Tên Công Việc' to 'Ghi Chú')
                empty_rows = [['' for _ in range(10)] for _ in range(num_rows_to_clear)]

                # Clear range A2:J(last_row)
                range_to_clear = f'A2:J{last_row}'

                # Update the range with empty values
                management_sheet.update(range_to_clear, empty_rows)
                logger.info(f"Cleared {num_rows_to_clear} rows from management sheet")
    
    def aggregate_data(self):
        """Aggregate data from all project sheets to the management sheet."""
        logger.info("Starting data aggregation...")

        # Get all project sheets
        project_sheets = self.get_project_sheets()

        # Gather all project data
        all_project_data = []
        all_project_content = []  # For hashing purposes

        # Process each project sheet
        for project_sheet in project_sheets:
            logger.info(f"Processing project sheet: {project_sheet.title}")

            # Get all values from the project sheet
            project_rows = project_sheet.get_all_values()

            if not project_rows:
                logger.info(f"Project sheet '{project_sheet.title}' is empty, skipping.")
                continue

            # Store project sheet content for hashing
            all_project_content.extend([project_sheet.title] + project_rows)

            # Get the header row from the project sheet
            project_header = project_rows[0]
            project_data = project_rows[1:]  # Exclude the header row

            # Map project sheet columns to management sheet columns
            # Management header: ['Tên Công Việc', 'Dự Án', 'Loại Công Việc', 'Phụ Trách', 'Trạng Thái', 'Ngày Bắt Đầu', 'Ngày Kết Thúc', 'Ngày Hoàn Thành', 'Link Sản Phẩm', 'Ghi Chú']
            # Example project header: ['Tên Công Việc', 'Loại Công Việc', 'Phụ Trách', 'Trạng Thái', 'Ngày Bắt Đầu', 'Ngày Kết Thúc', 'Ngày Hoàn Thành', 'Link Sản Phẩm', 'Ghi Chú']

            name_idx = find_column_index(project_header, ['Tên Công Việc', 'Task Name', 'Job Title'])
            type_idx = find_column_index(project_header, ['Loại Công Việc', 'Task Type', 'Work Type'])
            responsible_idx = find_column_index(project_header, ['Phụ Trách', 'Responsible', 'Assignee'])
            status_idx = find_column_index(project_header, ['Trạng Thái', 'Status', 'State'])
            start_date_idx = find_column_index(project_header, ['Ngày Bắt Đầu', 'Start Date', 'Begin Date'])
            end_date_idx = find_column_index(project_header, ['Ngày Kết Thúc', 'End Date', 'Finish Date'])
            completion_date_idx = find_column_index(project_header, ['Ngày Hoàn Thành', 'Completion Date', 'Date Completed'])
            link_idx = find_column_index(project_header, ['Link Sản Phẩm', 'Product Link', 'URL'])
            note_idx = find_column_index(project_header, ['Ghi Chú', 'Notes', 'Comment'])

            # Process each row in the project sheet
            for row in project_data:
                if len(row) == 0:
                    continue  # Skip empty rows

                # Build management row with mapped values
                management_row = [''] * 10  # 10 columns in management sheet

                # Fill the mapped columns
                if name_idx is not None and name_idx < len(row):
                    management_row[0] = row[name_idx]  # Tên Công Việc
                management_row[1] = project_sheet.title  # Dự Án (set to project sheet name)
                if type_idx is not None and type_idx < len(row):
                    management_row[2] = row[type_idx]  # Loại Công Việc
                if responsible_idx is not None and responsible_idx < len(row):
                    management_row[3] = row[responsible_idx]  # Phụ Trách
                if status_idx is not None and status_idx < len(row):
                    management_row[4] = row[status_idx]  # Trạng Thái
                if start_date_idx is not None and start_date_idx < len(row):
                    management_row[5] = row[start_date_idx]  # Ngày Bắt Đầu
                if end_date_idx is not None and end_date_idx < len(row):
                    management_row[6] = row[end_date_idx]  # Ngày Kết Thúc
                if completion_date_idx is not None and completion_date_idx < len(row):
                    management_row[7] = row[completion_date_idx]  # Ngày Hoàn Thành
                if link_idx is not None and link_idx < len(row):
                    management_row[8] = row[link_idx]  # Link Sản Phẩm
                if note_idx is not None and note_idx < len(row):
                    management_row[9] = row[note_idx]  # Ghi Chú

                all_project_data.append(management_row)

        # Create a hash of the current project data
        current_data_str = str(all_project_content)
        current_data_hash = hashlib.md5(current_data_str.encode()).hexdigest()

        # Check if the data has changed since the last update
        data_changed = self.previous_data_hash != current_data_hash
        self.previous_data_hash = current_data_hash

        if data_changed:
            logger.info("Project data has changed, updating management sheet...")

            # Get the management sheet
            management_sheet = self.get_worksheet_by_name(self.management_sheet_name)

            # Clear the management sheet (keeping the header)
            self.clear_management_sheet(management_sheet)

            # Define the header for the management sheet
            management_header = ['Tên Công Việc', 'Dự Án', 'Loại Công Việc', 'Phụ Trách', 'Trạng Thái', 'Ngày Bắt Đầu', 'Ngày Kết Thúc', 'Ngày Hoàn Thành', 'Link Sản Phẩm', 'Ghi Chú']

            # Update the header row (row 1)
            management_sheet.update('A1:J1', [management_header])

            # Add all project data to the management sheet
            if all_project_data:
                # Update starting from row 2 (after header)
                start_row = 2
                end_row = start_row + len(all_project_data) - 1
                range_name = f'A{start_row}:J{end_row}'
                management_sheet.update(range_name, all_project_data)

            logger.info(f"Updated management sheet with {len(all_project_data)} rows from {len(project_sheets)} project sheets")
        else:
            logger.info("No changes detected in project sheets, skipping management sheet update")
    
    
    def run(self):
        """Run the dashboard aggregation loop."""
        logger.info(f"Starting Project Dashboard with update interval: {self.update_interval}s")
        
        # Initialize the connection
        self.initialize_connection()
        
        while True:
            try:
                self.aggregate_data()
                logger.info(f"Waiting {self.update_interval} seconds before next update...")
                time.sleep(self.update_interval)
            except KeyboardInterrupt:
                logger.info("Dashboard stopped by user.")
                break
            except Exception as e:
                logger.error(f"Error during aggregation: {str(e)}")
                logger.info(f"Retrying in {self.update_interval} seconds...")
                time.sleep(self.update_interval)

def main():
    """Main entry point."""
    # Validate configuration
    Config.validate()

    # Use the configured update interval
    dashboard = ProjectDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()