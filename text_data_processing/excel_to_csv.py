import pandas as pd

excel_path = "Output_Data_Structure.xlsx"    # Excel file path

excel_file = pd.read_excel(excel_path)      # Reading excel file

excel_file.to_csv("Output_Data_Structure.csv", index=None, header=True)     # Converting excel to csv