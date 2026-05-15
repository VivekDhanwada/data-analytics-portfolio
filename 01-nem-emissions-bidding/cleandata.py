import pandas as pd

# 1. Load both Excel files
df_2019 = pd.read_excel("Bidstack-April2019.xlsx", sheet_name="Bidstack-April2019")
df_2025 = pd.read_excel("Bidstack-April2025.xlsx", sheet_name="Bidstack-April2025")

# 2. Add a Year column
df_2019['Year'] = 2019
df_2025['Year'] = 2025

# 3. Combine both years
df = pd.concat([df_2019, df_2025], ignore_index=True)

# 4. Melt price and volume columns
price_cols = [f'PRICEBAND{i}' for i in range(1, 11)]
volume_cols = [f'BANDAVAIL{i}' for i in range(1, 11)]

df_prices = df.melt(id_vars=['INTERVAL_DATETIME', 'DUID', 'Region', 'Generation Type', 'Year'],
                    value_vars=price_cols,
                    var_name='PriceBand',
                    value_name='Price')

df_volumes = df.melt(id_vars=['INTERVAL_DATETIME', 'DUID', 'Region', 'Generation Type', 'Year'],
                     value_vars=volume_cols,
                     var_name='VolumeBand',
                     value_name='Volume')

# 5. Align bands
df_prices['BandIndex'] = df_prices['PriceBand'].str.extract('(\d+)').astype(int)
df_volumes['BandIndex'] = df_volumes['VolumeBand'].str.extract('(\d+)').astype(int)

# 6. Merge price and volume into one long-form table
df_long = pd.merge(
    df_prices.drop(columns='PriceBand'),
    df_volumes.drop(columns=['VolumeBand', 'INTERVAL_DATETIME', 'DUID', 'Region', 'Generation Type', 'Year']),
    left_index=True,
    right_index=True
)

# 7. Add time fields
df_long['Hour'] = pd.to_datetime(df_long['INTERVAL_DATETIME']).dt.hour

def time_of_day(hour):
    if 0 <= hour < 6:
        return 'Night'
    elif 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

df_long['Time of Day'] = df_long['Hour'].apply(time_of_day)

# 8. Create Generator Grouping
def group_gen(gt):
    gt = str(gt).lower()
    if "solar" in gt or "wind" in gt:
        return "Renewable"
    elif "hydro" in gt:
        return "Hydro"
    else:
        return "Fossil"

df_long['Gen Group'] = df_long['Generation Type'].apply(group_gen)

# 9. Final columns
df_final = df_long[[
    'INTERVAL_DATETIME', 'Year', 'Hour', 'Time of Day', 'DUID',
    'Region', 'Generation Type', 'Gen Group', 'Price', 'Volume'
]]

# 10. Save to CSV for Tableau
df_final.to_csv("Cleaned_Bidding_Data_2019_2025.csv", index=False)