import pandas as pd
import numpy as np
def read_indicator(dd1,dd2,dd3):
    # dd1: Name of file
    # dd2: Name of sheet
    # dd3: Name of indicator

    # df contains the whole sheet that you are interesting in
    df = pd.read_excel(dd1, sheet_name=dd2, engine='openpyxl')
    return df[dd3]