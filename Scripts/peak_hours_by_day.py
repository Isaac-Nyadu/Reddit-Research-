import pandas as pd
import matplotlib.pyplot as plt
import pytz
import os

# Step 1: Read the CSV file
df = pd.read_csv('../Loneliness_Post/Loneliness Yearly Posts.csv')

# Step 2: Convert 'created_utc' to datetime with UTC timezone
df['created_utc'] = pd.to_datetime(df['created_utc'], utc=True)

# Step 3: Convert 'created_utc' to US/Eastern timezone
eastern = pytz.timezone('US/Eastern')
df['created_utc'] = df['created_utc'].dt.tz_convert(eastern)

# Step 4: Extract the day of the week from 'created_utc'
df['day_of_week'] = df['created_utc'].dt.day_name()

# Step 5: Count the number of posts per day of the week
day_counts = df['day_of_week'].value_counts()

# Step 6: Reorder the days to Monday through Sunday
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = day_counts.reindex(day_order)

# Step 7: Plot the results
plt.figure(figsize=(8,6))
day_counts.plot(kind='bar', color='coral')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Posts')
plt.title('Reddit Posts by Day of the Week')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Step 8: Create directory if it doesn't exist
output_dir = '../Images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 9: Save the plot to a file
plt.savefig(f'{output_dir}/reddit_posts_by_day.png', dpi=300)

# Optional: Display the plot
plt.show()
