import openpyxl
import pandas as pd
# easy way to write in a specific part of an excel sheet
def write_excel2(df,file,sheet,startrow,startcol):
    book = openpyxl.load_workbook(file)
    writer = pd.ExcelWriter(file, engine='openpyxl') 
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    df.to_excel(writer, sheet_name=sheet,startrow=startrow,startcol=startcol, index=False, index_label=False, header=True)
    book.save(file)