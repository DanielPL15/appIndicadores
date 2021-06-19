import openpyxl

def deleteSheet(route,sheet):
    workbook=openpyxl.load_workbook(route)

    std=workbook.get_sheet_by_name(sheet)

    workbook.remove_sheet(std)

    workbook.save(route)

