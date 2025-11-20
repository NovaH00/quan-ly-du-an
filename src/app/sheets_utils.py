"""
Utility functions for Google Sheets operations
"""

import logging
from typing import List, Optional
import gspread

logger = logging.getLogger(__name__)

def find_column_index(header_row: List[str], target_names: List[str]) -> Optional[int]:
    """
    Find the index of a column by looking for any of the target names in the header row.
    
    Args:
        header_row: List of column names in the header row
        target_names: List of possible names for the column we're looking for
        
    Returns:
        Index of the column if found, None otherwise
    """
    for i, header in enumerate(header_row):
        if header in target_names:
            return i
    return None

def num_to_col_name(n):
    """Convert column number to Excel column name (1 -> A, 27 -> AA)"""
    result = ""
    n -= 1  # 0-indexed
    while n >= 0:
        result = chr(n % 26 + ord('A')) + result
        n = n // 26 - 1
    return result

def ensure_worksheet_exists(spreadsheet, name: str, rows: int = 1000, cols: int = 7):
    """
    Get a worksheet by name, creating it if it doesn't exist.
    
    Args:
        spreadsheet: The spreadsheet object
        name: Name of the worksheet
        rows: Number of rows to create if worksheet is new
        cols: Number of columns to create if worksheet is new
        
    Returns:
        The worksheet object
    """
    try:
        return spreadsheet.worksheet(name)
    except gspread.exceptions.WorksheetNotFound:
        logger.info(f"Worksheet '{name}' not found. Creating it...")
        return spreadsheet.add_worksheet(title=name, rows=str(rows), cols=str(cols))