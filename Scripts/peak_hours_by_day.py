import pandas as pd
import matplotlib.pyplot as plt
import pytz
import os

df = pd.read_csv('../Loneliness_Post/Loneliness Yearly Posts.csv')

df['created_utc'] = pd.to_datetime(df['created_utc'], utc=True)

eastern = pytz.timezone('US/Eastern')
df['created_utc'] = df['created_utc'].dt.tz_convert(eastern)

df['day_of_week'] = df['created_utc'].dt.day_name()

day_counts = df['day_of_week'].value_counts()

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_counts = day_counts.reindex(day_order)

plt.figure(figsize=(8,6))
day_counts.plot(kind='bar', color='coral')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Posts')
plt.title('Reddit Posts by Day of the Week')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.tight_layout()

output_dir = '../Images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

plt.savefig(f'{output_dir}/reddit_posts_by_day.png', dpi=300)

plt.show()
