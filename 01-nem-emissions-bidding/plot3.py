import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned bidding data
df = pd.read_csv("Cleaned_Bidding_Data_2019_2025.csv")

# Optional: Keep only bids with volume > 0
df = df[df['Volume'] > 0]

# Set Seaborn theme
sns.set(style="whitegrid")

# Set up the figure
plt.figure(figsize=(12, 6))

# Create the boxplot
sns.boxplot(data=df, x='Gen Group', y='Price', hue='Year')

# Formatting
plt.title("Bid Price Distribution by Generator Type and Year", fontsize=14)
plt.xlabel("Generator Group")
plt.ylabel("Bid Price ($/MWh)")
plt.ylim(-1500, 20000)  # Adjust if needed to show extreme bids
plt.legend(title='Year')
plt.tight_layout()

# Optional save
# plt.savefig("Boxplot_Bid_Price_by_Group_Year.png", dpi=300)

plt.show()