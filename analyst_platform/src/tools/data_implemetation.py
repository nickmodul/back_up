import pandas as pd
from pathlib import Path
# TASK: создать папку свалку / разработки для [default path]

def create_csv_process(
        path_intro,
        TABLES:dict
):
    for sheet_name,_data_frame in TABLES.items():
        path_csv = f"{sheet_name}.csv"
        _data_frame.to_csv(Path(path_intro/ path_csv))

def create_xlsx_process(
        path_intro,
        xlsx_name:str,
        TABLES:dict
):  
    norm_path = f'{xlsx_name}.xlsx'
    
    with pd.ExcelWriter(Path(path_intro/ norm_path)) as writer:  
        for sheet_name,_data_frame in TABLES.items():
            _data_frame.to_excel(writer, sheet_name=sheet_name)