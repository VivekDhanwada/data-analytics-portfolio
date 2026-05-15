import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your cleaned file
df = pd.read_csv("Cleaned_Bidding_Data_2019_2025.csv")

# Optional: Filter out zero-volume bids
df = df[df['Volume'] > 0]

# Calculate volume-weighted average price per hour, year, and gen group
grouped = (
    df.groupby(['Year', 'Hour', 'Gen Group'])
    .apply(lambda x: (x['Price'] * x['Volume']).sum() / x['Volume'].sum())
    .reset_index(name='Volume Weighted Price')
)

# Set plot style
sns.set(style="whitegrid")

# Create lineplot
plt.figure(figsize=(12, 6))
sns.lineplot(data=grouped, x='Hour', y='Volume Weighted Price', hue='Year', style='Gen Group', markers=True)

# Labels and formatting
plt.title("Volume-Weighted Average Bid Price by Hour (2019 vs 2025)", fontsize=14)
plt.xlabel("Hour of Day")
plt.ylabel("Avg Bid Price ($/MWh)")
plt.xticks(range(0, 24))
plt.legend(title="Year / Gen Group")
plt.tight_layout()

# Save the figure if needed
# plt.savefig("Bid_Price_by_Hour.png", dpi=300)

plt.show()