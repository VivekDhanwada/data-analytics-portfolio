import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned bidding data
df = pd.read_csv("Cleaned_Bidding_Data_2019_2025.csv")

# Optional: filter out zero-volume bids
df = df[df['Volume'] > 0]

# Calculate volume-weighted average price by Hour and Gen Group
heatmap_data = (
    df.groupby(['Hour', 'Gen Group'])
    .apply(lambda x: (x['Price'] * x['Volume']).sum() / x['Volume'].sum())
    .reset_index(name='Volume Weighted Price')
)

# Pivot for heatmap structure (Gen Group = rows, Hour = columns)
heatmap_pivot = heatmap_data.pivot(index='Gen Group', columns='Hour', values='Volume Weighted Price')

# Create the heatmap
plt.figure(figsize=(12, 4))
sns.heatmap(heatmap_pivot, annot=True, fmt=".0f", cmap="coolwarm", center=0, linewidths=0.5, linecolor='gray')

# Formatting
plt.title("Volume-Weighted Price by Hour and Generator Group", fontsize=14)
plt.xlabel("Hour of Day")
plt.ylabel("Generator Group")
plt.tight_layout()

# Optional save
# plt.savefig("Heatmap_Bid_Price_by_Hour_GenGroup.png", dpi=300)

plt.show()