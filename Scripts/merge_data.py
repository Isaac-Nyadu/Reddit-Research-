import pandas as pd
import glob
import os

# Define the path to your data directory
data_path = '../Loneliness_Post/'

# Create a pattern to match all CSV files in the directory
file_pattern = os.path.join(data_path, 'sub_2022_??_lonely_AA.csv')
print(file_pattern)

# Get a sorted list of all matching CSV files
file_list = sorted(glob.glob(file_pattern))

# Initialize an empty list to hold dataframes
df_list = []

# Iterate over each file and read it into a dataframe
for file in file_list:
    try:
        df = pd.read_csv(file)
        df_list.append(df)
        print(f"Successfully read {file}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

print(df_list)
# Concatenate all dataframes into one
merged_df = pd.concat(df_list, ignore_index=True)

# Define the output file path
output_file = os.path.join(data_path, 'Loneliness Yearly Posts.csv')

# Save the merged dataframe to a new CSV file
merged_df.to_csv(output_file, index=False)

print(f"All files have been merged into {output_file}")
