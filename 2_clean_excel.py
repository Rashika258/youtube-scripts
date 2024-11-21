import os
import pandas as pd

# Path to your Excel file
excel_file = r'C:\Users\rashi\Downloads\audio_sorted.xlsx'

# Load the Excel file
df = pd.read_excel(excel_file)

# Check if the file path exists for each row and filter out rows where the path is missing
df = df[df['File Path'].apply(lambda path: os.path.exists(path) if pd.notnull(path) else False)]

# Save the updated DataFrame back to the Excel file, overwriting it
df.to_excel(excel_file, index=False)

print("Rows with missing file paths have been removed.")
