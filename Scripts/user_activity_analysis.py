import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import hashlib

# Step 1: Read the CSV file
df = pd.read_csv('../Loneliness_Post/Loneliness Yearly Posts.csv')
# Step 2: Data Cleaning and Preparation

# Remove rows with missing 'user_id' or 'num_comments'
df = df.dropna(subset=['user_id', 'num_comments'])

# Convert 'num_comments' to numeric
df['num_comments'] = pd.to_numeric(df['num_comments'], errors='coerce')

# Drop any rows where 'num_comments' could not be converted
df = df.dropna(subset=['num_comments'])

# Remove posts by '[deleted]' users
df = df[df['user_id'] != '[deleted]']

# Step 3: Calculate Number of Posts per User
posts_per_user = df.groupby('user_id').size().reset_index(name='num_posts')

# Step 4: Calculate Total Comments Received per User
comments_per_user = df.groupby('user_id')['num_comments'].sum().reset_index(name='total_comments_received')

# Step 5: Merge the DataFrames
user_activity = pd.merge(posts_per_user, comments_per_user, on='user_id')

# Step 6: Analyze the Relationship between Posts and Comments

# Scatter Plot
plt.figure(figsize=(10,6))
sns.scatterplot(data=user_activity, x='num_posts', y='total_comments_received', alpha=0.5)
plt.xlabel('Number of Posts per User')
plt.ylabel('Total Comments Received')
plt.title('Relationship Between User Posts and Comments Received')
plt.grid(True)
plt.tight_layout()

# Save the plot
output_dir = 'output_plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

plt.savefig(f'{output_dir}/posts_vs_comments_scatter.png', dpi=300)
plt.show()

# Calculate Correlation Coefficient
correlation = user_activity['num_posts'].corr(user_activity['total_comments_received'])
print(f"Correlation between number of posts and total comments received: {correlation:.2f}")

# Step 7: Analyze Posting Frequency Over Time

# Convert 'created_utc' to datetime
df['created_utc'] = pd.to_datetime(df['created_utc'], utc=True)

# Calculate first and last post dates per user
user_dates = df.groupby('user_id')['created_utc'].agg(['min', 'max']).reset_index()
user_dates['posting_duration_days'] = (user_dates['max'] - user_dates['min']).dt.days + 1

# Merge with user_activity
user_activity = pd.merge(user_activity, user_dates[['user_id', 'posting_duration_days']], on='user_id')

# Calculate average posts per day
user_activity['posts_per_day'] = user_activity['num_posts'] / user_activity['posting_duration_days']

# Step 8: Distribution of User Posting Frequency

# Histogram of posts per day
plt.figure(figsize=(10,6))
sns.histplot(user_activity['posts_per_day'], bins=50, kde=True)
plt.xlabel('Average Posts per Day per User')
plt.title('Distribution of User Posting Frequency')
plt.tight_layout()
plt.savefig(f'{output_dir}/posts_per_day_histogram.png', dpi=300)
plt.show()

# Step 9: Relationship Between Posts per Day and Comments Received

# Scatter Plot
plt.figure(figsize=(10,6))
sns.scatterplot(data=user_activity, x='posts_per_day', y='total_comments_received', alpha=0.5)
plt.xlabel('Average Posts per Day per User')
plt.ylabel('Total Comments Received')
plt.title('Posts per Day vs. Total Comments Received')
plt.grid(True)
plt.tight_layout()
plt.savefig(f'{output_dir}/posts_per_day_vs_comments_scatter.png', dpi=300)
plt.show()

# Step 10: Log Transformation for Skewed Data

# Apply log transformation
user_activity['log_num_posts'] = np.log1p(user_activity['num_posts'])
user_activity['log_total_comments'] = np.log1p(user_activity['total_comments_received'])

# Scatter Plot of Log-Transformed Data
plt.figure(figsize=(10,6))
sns.scatterplot(data=user_activity, x='log_num_posts', y='log_total_comments', alpha=0.5)
plt.xlabel('Log(Number of Posts per User)')
plt.ylabel('Log(Total Comments Received)')
plt.title('Log-Transformed Relationship Between Posts and Comments')
plt.grid(True)
plt.tight_layout()
plt.savefig(f'{output_dir}/log_posts_vs_log_comments_scatter.png', dpi=300)
plt.show()

# Step 11: Calculate Average Comments per Post per User

user_activity['avg_comments_per_post'] = user_activity['total_comments_received'] / user_activity['num_posts']

# Scatter Plot
plt.figure(figsize=(10,6))
sns.scatterplot(data=user_activity, x='num_posts', y='avg_comments_per_post', alpha=0.5)
plt.xlabel('Number of Posts per User')
plt.ylabel('Average Comments per Post')
plt.title('Average Comments per Post vs. Number of Posts per User')
plt.grid(True)
plt.tight_layout()
plt.savefig(f'{output_dir}/avg_comments_per_post_vs_num_posts.png', dpi=300)
plt.show()

# Step 12: Anonymize user_id (Optional)
# If you wish to anonymize user IDs for privacy, uncomment the following lines

# user_activity['user_id'] = user_activity['user_id'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())

# Step 13: Save the user_activity DataFrame to a CSV File

user_activity.to_csv('user_activity_analysis.csv', index=False)

print("Analysis complete. Results saved to 'user_activity_analysis.csv' and plots saved in the 'output_plots' directory.")
