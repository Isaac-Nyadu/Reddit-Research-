import pandas as pd
import glob
import os

data_path = '../Loneliness_Post/'

file_pattern = os.path.join(data_path, 'sub_2022_??_lonely_AA.csv')
print(file_pattern)

file_list = sorted(glob.glob(file_pattern))

df_list = []

for file in file_list:
    try:
        df = pd.read_csv(file)
        df_list.append(df)
        print(f"Successfully read {file}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

print(df_list)

merged_df = pd.concat(df_list, ignore_index=True)

output_file = os.path.join(data_path, 'Loneliness Yearly Posts.csv')

merged_df.to_csv(output_file, index=False)

print(f"All files have been merged into {output_file}")
