# Project Management Dashboard

This application aggregates data from multiple project sheets into a central management sheet in Google Sheets.

## How it Works

- The application identifies one sheet as the "management sheet" (default name: `Quản Lý`)
- All other sheets are treated as "project sheets"
- Every `N` seconds (default: 10s), the application:
  1. Reads all data from project sheets
  2. Creates a hash of the current project data to detect changes
  3. If there are changes in the project sheets:
     - Maps relevant columns to the management sheet format
     - Clears the management sheet (preserving headers)
     - Writes aggregated data to the management sheet
     - Sets the "Dự Án" (Project) field to the name of the source sheet
  4. If no changes detected, skips updating the management sheet to save API calls

## Configuration

The application uses the following environment variables:

- `GOOGLE_SHEET_ID`: Google Sheets document ID
- `CREDENTIALS`: Path to the service account credentials JSON file
- `UPDATE_INTERVAL`: Update interval in seconds (default: 10)
- `MANAGEMENT_SHEET_NAME`: Name of the management sheet (default: `Quản Lý`)

## Column Mapping

The application maps columns from project sheets to the management sheet:

Management Sheet Columns: `['Tên Công Việc', 'Dự Án', 'Loại Công Việc', 'Phụ Trách', 'Trạng Thái', 'Ngày Bắt Đầu', 'Ngày Kết Thúc', 'Ngày Hoàn Thành', 'Link Sản Phẩm', 'Ghi Chú']`

The application looks for equivalent column names in project sheets:
- `Tên Công Việc`: 'Tên Công Việc', 'Task Name', 'Job Title'
- `Loại Công Việc`: 'Loại Công Việc', 'Task Type', 'Work Type'
- `Phụ Trách`: 'Phụ Trách', 'Responsible', 'Assignee'
- `Trạng Thái`: 'Trạng Thái', 'Status', 'State'
- `Ngày Bắt Đầu`: 'Ngày Bắt Đầu', 'Start Date', 'Begin Date'
- `Ngày Kết Thúc`: 'Ngày Kết Thúc', 'End Date', 'Finish Date'
- `Ngày Hoàn Thành`: 'Ngày Hoàn Thành', 'Completion Date', 'Date Completed'
- `Link Sản Phẩm`: 'Link Sản Phẩm', 'Product Link', 'URL'
- `Ghi Chú`: 'Ghi Chú', 'Notes', 'Comment'

## Usage

Run the application with:

```bash
python main.py
```

The application will run continuously, updating at the specified interval.