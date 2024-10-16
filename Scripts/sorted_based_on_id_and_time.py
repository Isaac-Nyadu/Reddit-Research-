import pandas as pd
import os

df = pd.read_csv('../Loneliness_Post/Loneliness Yearly Posts.csv')

df['created_utc'] = pd.to_datetime(df['created_utc'], utc=True, errors='coerce')

df = df.dropna(subset=['user_id', 'created_utc'])

df = df[df['user_id'] != '[deleted]']

df_sorted = df.sort_values(by=['user_id', 'created_utc'])

df_sorted = df_sorted.reset_index(drop=True)

output_dir = '../Results CSVs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, 'sorted_Loneliness_Yearly_Posts.csv')


df_sorted.to_csv(output_file, index=False)

print(f"Data has been sorted and saved to '{output_file}'.")
