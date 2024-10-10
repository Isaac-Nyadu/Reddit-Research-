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

# Step 4: Extract the hour from 'created_utc'
df['hour'] = df['created_utc'].dt.hour

# Step 5: Count the number of posts per hour
hourly_counts = df.groupby('hour').size().sort_index()

# Step 6: Plot the results
plt.figure(figsize=(10,6))
hourly_counts.plot(kind='bar', color='skyblue')
plt.xlabel('Hour of the Day (US/Eastern)')
plt.ylabel('Number of Posts')
plt.title('Reddit Posts by Hour of the Day in Eastern Time')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Step 7: Create directory if it doesn't exist
output_dir = os.path.abspath('../Images')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directory created: {output_dir}")
else:
    print(f"Directory exists: {output_dir}")

# Step 8: Save the plot to a file with error handling
output_file = os.path.join(output_dir, 'reddit_posts_by_hour.png')
try:
    plt.savefig(output_file, dpi=300)
    print(f"Image saved successfully at {output_file}")
except Exception as e:
    print("Error saving image:", e)

# Optional: Display the plot
plt.show()