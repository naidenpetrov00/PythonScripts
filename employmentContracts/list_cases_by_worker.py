import pandas as pd
import os

folder_path = "./documents"
responsible_prop = "Отговорен"

for filename in os.listdir(folder_path):
    if filename.endswith(".ods"):
        file_path = os.path.join(folder_path, filename)
        print(f"Reading: {file_path}")
        try:
            df = pd.read_excel(file_path)
            df = df.sort_values(by=responsible_prop)
            print(df)
        except Exception as e:
            print(f"Error Reading: {file_path}")
            print(e)