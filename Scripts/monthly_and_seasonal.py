import pandas as pd
import matplotlib.pyplot as plt
import pytz
import os

# Read the CSV file
df = pd.read_csv('../Loneliness_Post/Loneliness Yearly Posts.csv')

# Convert 'created_utc' to datetime with UTC timezone
df['created_utc'] = pd.to_datetime(df['created_utc'], utc=True)

# Convert 'created_utc' to US/Eastern timezone
eastern = pytz.timezone('US/Eastern')
df['created_utc'] = df['created_utc'].dt.tz_convert(eastern)

# Create output directory if it doesn't exist
output_dir = '../Images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    print(f"Directory exists: {output_dir}")

### Monthly Analysis ###

# Extract month
df['month'] = df['created_utc'].dt.month_name()

# Count posts per month
month_counts = df['month'].value_counts()
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
month_counts = month_counts.reindex(month_order)

# Plot monthly results
plt.figure(figsize=(10,6))
month_counts.plot(kind='bar', color='mediumseagreen')
plt.xlabel('Month')
plt.ylabel('Number of Posts')
plt.title('Reddit Posts by Month')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Save monthly plot
plt.savefig(f'{output_dir}/reddit_posts_by_month.png', dpi=300)
print(f"Monthly image saved at {output_dir}/reddit_posts_by_month.png")
plt.show()

### Seasonal Analysis ###

# Define seasons
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Fall'

# Apply the function to create a 'season' column
df['season'] = df['created_utc'].apply(get_season)

# Count posts per season
season_counts = df['season'].value_counts()
season_order = ['Winter', 'Spring', 'Summer', 'Fall']
season_counts = season_counts.reindex(season_order)

# Plot seasonal results
plt.figure(figsize=(8,6))
season_counts.plot(kind='bar', color='orchid')
plt.xlabel('Season')
plt.ylabel('Number of Posts')
plt.title('Reddit Posts by Season')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.tight_layout()

# Save seasonal plot
plt.savefig(f'{output_dir}/reddit_posts_by_season.png', dpi=300)
print(f"Seasonal image saved at {output_dir}/reddit_posts_by_season.png")
plt.show()
