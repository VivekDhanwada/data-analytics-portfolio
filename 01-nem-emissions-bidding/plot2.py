import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("Cleaned_Bidding_Data_2019_2025.csv")

# Optional: filter to bids with volume > 0
df = df[df['Volume'] > 0]

# Sort and build cumulative volume within each group
def get_supply_curve(data, year, gen_group):
    df_filtered = data[(data['Year'] == year) & (data['Gen Group'] == gen_group)]
    df_sorted = df_filtered.sort_values(by='Price')
    df_sorted['Cumulative Volume'] = df_sorted['Volume'].cumsum()
    return df_sorted

# Define curve segments
groups = ['Fossil', 'Renewable']
years = [2019, 2025]

# Plot setup
plt.figure(figsize=(12, 6))
colors = {'Fossil': 'firebrick', 'Renewable': 'forestgreen'}
linestyles = {2019: 'dashed', 2025: 'solid'}

for group in groups:
    for year in years:
        curve = get_supply_curve(df, year, group)
        plt.plot(curve['Cumulative Volume'], curve['Price'],
                 label=f"{group} ({year})",
                 color=colors[group],
                 linestyle=linestyles[year])

# Format
plt.title("Supply Curve: Price vs Cumulative Volume (2019 vs 2025)", fontsize=14)
plt.xlabel("Cumulative Volume (MW)")
plt.ylabel("Bid Price ($/MWh)")
plt.legend(title="Gen Group + Year")
plt.grid(True)
plt.tight_layout()

# Save optional
# plt.savefig("Supply_Curve_2019_2025.png", dpi=300)

plt.show()