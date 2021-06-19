import openpyxl
from openpyxl import load_workbook


def deleteColums(file,sheet,starting_column,last_column):
    wb = load_workbook(filename = file)
    sheet = wb[sheet]

    possible_columns = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','X','Y','Z']
    for row in sheet[possible_columns[starting_column]+'1:'+possible_columns[last_column]+'400']:
        for cell in row:
            cell.value = ''
    wb.save(file)

