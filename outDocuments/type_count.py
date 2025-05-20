import pandas as pd
import os
from collections import defaultdict

folder_path = "./documents"
main_type_prop = "Тип"
inner_type_prop = "Подтип"

def write_counts(result: defaultdict[any, defaultdict[any, int]], file_name: str): # type: ignore
    output = {}
    for main_type,inner_type in result.items():
        sorted_items = sorted(inner_type.items(), key=lambda x: x[1],reverse=True)
        output[main_type] = dict(sorted_items)
    with open(f'results/{file_name}.txt', 'w') as f:
        f.write(f"                  Изходирани документи за {file_name}\n")
        for main_type, inner_dict in output.items():
            total_count = sum(inner_dict.values())
            f.write(f"  {main_type} (общо: {total_count} документа):\n")
            for inner_type, count in inner_dict.items():
                f.write(f"          {inner_type}: {count},\n")

for file_name in os.listdir(folder_path):
    result = defaultdict(lambda: defaultdict(int))
    if file_name.endswith('.ods'):
        file_path = os.path.join(folder_path, file_name)
        print(f"Reading: {file_path}")
        try:
            df = pd.read_excel(file_path, engine='odf')
            for index, row in df.iterrows():
                main_type = row[main_type_prop]
                inner_type = row[inner_type_prop]
                result[main_type][inner_type] += 1
            
            write_counts(result, file_name.removesuffix('.ods'))
        except Exception as e:
            print(f"Error reading {file_path}")
