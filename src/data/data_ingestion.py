
import pandas as pd
import glob
import os

# Folder where your .xlsx files are located
folder_path = 'data/scrapped'

# Get list of all .xlsx files in the folder
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))

# List to hold individual DataFrames
dfs = []

for file in excel_files:
    df = pd.read_excel(file)
    # Optional: Add a column to track which file it came from (e.g., 'mobile', 'laptop')
    df['Category'] = os.path.basename(file).replace('.xlsx', '')
    dfs.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

os.makedirs('artifacts/data',exist_ok=True)
# os.makedirs('data')
merged_df.to_csv('artifacts/data/raw_data.csv', index=False)

# Optional: Save as one Excel file
# merged_df.to_excel('../data/final_data.xlsx', index=False)

# print("Merging completed! Files saved as 'merged_products.csv' and 'merged_products.xlsx'")

