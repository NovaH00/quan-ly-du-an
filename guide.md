This is the output when run the `./main.py` file. Use it as a reference
---
Found 2 sheets.
Reading sheet: Quản Lý
  - Headers/First Row: ['Tên Công Việc', 'Dự Án', 'Loại Công Việc', 'Phụ Trách', 'Trạng Thái', 'Link Sản Phẩm', 'Ghi Chú']
------------------------------
Reading sheet: Bling Kim
  - Headers/First Row: ['Tên Công Việc', 'Loại Công Việc', 'Phụ Trách', 'Trạng Thái', 'Ngày Bắt Đầu', 'Ngày Kết Thúc', 'Ngày Hoàn Thành', 'Link Sản Phẩm', 'Ghi Chú']
------------------------------
---

In the previous output, there are 2 types of sheets
- If the sheet's name is: Quản Lý. The sheet is the management sheet 
- For other sheets, their type is project sheet


I want all the information in the projects sheet row be aggregate into the management sheet (like a dashboard)

In the management sheet, the 'Dự Án' field is the name of the source sheet as mention

Omit other usused fields in the source sheets for now


The update previous is settable (default to every 10s). And I want update, meaning it retrieve every rows in every otehr sheet on every iternation and push it to the management sheet (to accomodate for the operation on the project sheets like edit, remvoe,....)
