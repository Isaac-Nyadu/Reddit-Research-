import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import hashlib

df = pd.read_csv('../Loneliness_Post/Loneliness Yearly Posts.csv')


df = df.dropna(subset=['user_id', 'num_comments'])

df['num_comments'] = pd.to_numeric(df['num_comments'], errors='coerce')


df = df.dropna(subset=['num_comments'])

df = df[df['user_id'] != '[deleted]']

posts_per_user = df.groupby('user_id').size().reset_index(name='num_posts')

comments_per_user = df.groupby('user_id')['num_comments'].sum().reset_index(name='total_comments_received')

user_activity = pd.merge(posts_per_user, comments_per_user, on='user_id')

filtered_users = user_activity[(user_activity['num_posts'] >= 1) & (user_activity['num_posts'] <= 10)]

category_1 = filtered_users[filtered_users['total_comments_received'] >= 50].copy()
category_1['category'] = '50 or more comments'

category_2 = filtered_users[filtered_users['total_comments_received'] <= 50].copy()
category_2['category'] = '50 or fewer comments'

combined_categories = pd.concat([category_1, category_2], ignore_index=True)

sns.set(style='whitegrid')

plt.figure(figsize=(10, 6))
sns.boxplot(x='category', y='num_posts', data=combined_categories)
plt.title('Number of Posts per User by Category')
plt.xlabel('Category')
plt.ylabel('Number of Posts')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='category', y='total_comments_received', data=combined_categories)
plt.title('Total Comments Received per User by Category')
plt.xlabel('Category')
plt.ylabel('Total Comments Received')
plt.tight_layout()
plt.show()

output_dir = 'filtered_users'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

category_1.to_csv(f'{output_dir}/users_with_1_to_10_posts_and_50_or_more_comments.csv', index=False)
category_2.to_csv(f'{output_dir}/users_with_1_to_10_posts_and_50_or_fewer_comments.csv', index=False)

print("Filtered users have been saved to the 'filtered_users' directory.")
