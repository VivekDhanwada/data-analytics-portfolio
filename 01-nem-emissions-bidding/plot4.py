import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned data
df = pd.read_csv("Cleaned_Bidding_Data_2019_2025.csv")

# Optional: Filter positive volume bids only
df = df[df['Volume'] > 0]

# Group by Year and Generator Group, then sum volume
volume_grouped = df.groupby(['Year', 'Gen Group'])['Volume'].sum().unstack()

# Plot as stacked bar
volume_grouped.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set2')

# Labels and formatting
plt.title("Total Bid Volume by Generator Group (2019 vs 2025)", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Total Volume (MW)")
plt.legend(title="Generator Group")
plt.tight_layout()

# Optional save
# plt.savefig("Stacked_Bid_Volume_by_Year.png", dpi=300)

plt.show()