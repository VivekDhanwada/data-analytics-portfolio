import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

MATCH_IDS = [3943043, 3942752, 3942226, 3941018, 3930179, 3930172, 3930160]
SPAIN_ID = 772

all_shots = []

for match_id in MATCH_IDS:
    events_url = f"{BASE_URL}/events/{match_id}.json"
    response = requests.get(events_url)
    events = response.json()
    
    for event in events:
        if event['type']['name'] == 'Shot' and event['team']['id'] == SPAIN_ID:
            event['match_id'] = match_id
            all_shots.append(event)

print(f"Total Spain shots: {len(all_shots)}") 

shot_data = []

for shot in all_shots:
    shot_data.append({
        'player': shot['player']['name'],
        'position': shot['position']['name'],
        'x': shot['location'][0],
        'y': shot['location'][1],
        'minute': shot['minute'],
        'xg': shot['shot']['statsbomb_xg'],
        'outcome': shot['shot']['outcome']['name'],
        'shot_type': shot['shot']['type']['name'],
        'body_part': shot['shot']['body_part']['name'],
        'match_id': shot['match_id']  
    })

df_shots = pd.DataFrame(shot_data)
print(df_shots.head())

df_shots.to_csv('spain-euro-2024/spain_shots.csv', index=False)
print("Saved: spain_shots.csv")

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

for _, shot in df_shots.iterrows():
    color = 'red' if shot['outcome'] == 'Goal' else 'white'
    size = shot['xg'] * 1000
    ax.scatter(shot['x'], shot['y'], c=color, s=size, alpha=0.7, zorder=3)

ax.set_title('Spain Euro 2024 — Shot Map', color='white', fontsize=16, pad=15)
ax.set_xlim(60, 120)
ax.set_ylim(0, 80)
ax.axis('off')


from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor='red', markersize=10, label='Goal'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor='white', markersize=10, label='No Goal'),
    Line2D([0], [0], marker='o', color='none', markerfacecolor='white', markersize=6, label='Size = xG value')
]
ax.legend(handles=legend_elements, loc='upper left', facecolor='#1a1a2e', labelcolor='white')

plt.savefig('spain-euro-2024/spain_shot_map.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.show()

from collections import Counter
outcomes = [e['shot']['outcome']['name'] for e in all_shots]
print(Counter(outcomes))