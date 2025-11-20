import gspread
import os

from src.utils import load_credentials

load_credentials()

# 1. Authenticate using your credentials file
# Replace 'credentials.json' with the actual path to your file
gc = gspread.service_account(filename=os.getenv("CREDENTIALS"))

# 2. Open the Spreadsheet by its ID
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sh = gc.open_by_key(SPREADSHEET_ID)

# 3. Loop through all worksheets (tabs) and read data
worksheet_list = sh.worksheets()

print(f"Found {len(worksheet_list)} sheets.")

data_storage = {}

for worksheet in worksheet_list:
    print(f"Reading sheet: {worksheet.title}")
    
    # Option A: Get all values as a list of lists (rows and columns)
    # Good for raw data or if you don't have headers in row 1
    rows = worksheet.get_all_values()
    
    # Option B: Get all records as a list of dictionaries
    # Good if Row 1 contains headers (keys)
    # records = worksheet.get_all_records()

    # Store the data
    data_storage[worksheet.title] = rows

    # Example: print first row of each sheet to verify
    if rows:
        print(f"  - Headers/First Row: {rows[0]}")
    print("-" * 30)

# Now 'data_storage' contains all your data:
# data_storage['Sheet1'] gives you the data for Sheet1
