import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

MATCH_IDS = [3943043, 3942752, 3942226, 3941018, 3930179, 3930172, 3930160]
SPAIN_ID = 772

all_press = []
all_recoveries = []

for match_id in MATCH_IDS:
    events_url = f"{BASE_URL}/events/{match_id}.json"
    response = requests.get(events_url)
    events = response.json()
    
    for event in events:
        if event['type']['name'] == 'Pressure' and event['team']['id'] == SPAIN_ID:
            event['match_id'] = match_id
            all_press.append(event)
        if event['type']['name'] == 'Ball Recovery' and event['team']['id'] == SPAIN_ID:
            event['match_id'] = match_id
            all_recoveries.append(event)

print(f"Total Spain presses: {len(all_press)}")
print(f"Total Spain ball recoveries: {len(all_recoveries)}")

press_data = []

for press in all_press:
    press_data.append({
        'x': press['location'][0],
        'y': press['location'][1],
        'match_id': press['match_id']  
    })
df_press = pd.DataFrame(press_data)
print(df_press.head())

recovery_data = []
for recovery in all_recoveries:
    recovery_data.append({
        'x': recovery['location'][0],
        'y': recovery['location'][1],
        'match_id': recovery['match_id']  
    })
df_recovery = pd.DataFrame(recovery_data)
print(df_recovery.head())

df_press.to_csv('spain-euro-2024/spain_press.csv', index=False)
df_recovery.to_csv('spain-euro-2024/spain_recovery.csv', index=False)
print("Saved: spain_press.csv and spain_recovery.csv")

fig, ax = plt.subplots(figsize=(8, 8))

# Pitch outline
ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#1a1a2e')

ax.plot([0, 0, 120, 120, 0], [0, 80, 80, 0, 0], color='white', linewidth=2)

# Halfway line
ax.plot([60, 60], [0, 80], color='white', linewidth=1)

# Penalty areas
ax.plot([102, 102, 120, 120, 102], [18, 62, 62, 18, 18], color='white', linewidth=1)
ax.plot([0, 0, 18, 18, 0], [18, 62, 62, 18, 18], color='white', linewidth=1)

# Goals
ax.plot([120, 120], [36, 44], color='white', linewidth=4)
ax.plot([0, 0], [36, 44], color='white', linewidth=4)

for _, press in df_press.iterrows():
    ax.scatter(press['x'], press['y'], c='orange', s=15, alpha=0.3, zorder=3)

for _, recovery in df_recovery.iterrows():
    ax.scatter(recovery['x'], recovery['y'], c='cyan', s=30, alpha=0.7, zorder=4)

ax.set_title('Spain Euro 2024 — Press & Ball Recovery Map', color='white', fontsize=16, pad=15)
ax.set_xlim(0, 120)
ax.set_ylim(0, 80)
ax.axis('off')

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor='orange', markersize=10, label='Pressure'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor='cyan', markersize=10, label='Ball Recovery')
]
ax.legend(handles=legend_elements, loc='upper left', facecolor='#1a1a2e', labelcolor='white')

plt.savefig('spain-euro-2024/spain_press_map.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')

median_press_x = df_press['x'].median()
ax.axvline(x=median_press_x, color='orange', linestyle='--', linewidth=1.5, alpha=0.8)
ax.text(median_press_x + 1, 5, f'Median press: x={median_press_x:.1f}', color='orange', fontsize=9)

plt.show()