import requests
import json

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMPETITION_ID = 55
SEASON_ID = 282

matches_url = f"{BASE_URL}/matches/{COMPETITION_ID}/{SEASON_ID}.json"
response = requests.get(matches_url)
matches = response.json()

print(f"Total matches in Euro 2024: {len(matches)}")

spain_matches = [m for m in matches if m["home_team"]["home_team_id"] == 772
                 or m["away_team"]["away_team_id"] == 772]

print(f"Spain matches: {len(spain_matches)}")

print(spain_matches)

for m in spain_matches:
    home = m['home_team']['home_team_name']
    away = m['away_team']['away_team_name']
    print(f"{m['match_date']} | {m['competition_stage']['name']} | {home} {m['home_score']}-{m['away_score']} {away} | ID: {m['match_id']}")

events_url = f"{BASE_URL}/events/3943043.json"
response = requests.get(events_url)
events = response.json()

import pandas as pd

df = pd.DataFrame(events)
print(df['type'].value_counts())

df['type_name'] = df['type'].apply(lambda x: x['name'])

for event_type, group in df.groupby('type_name'):
    has_location = group['location'].notna().any()
    print(f"{event_type} — location: {has_location}")

shots = df[df['type_name'] == 'Shot']
print(json.dumps(events[shots.index[0]], indent=2, ensure_ascii=False))

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 8))

ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#1a1a2e')

ax.plot([0, 0, 120, 120, 0], [0, 80, 80, 0, 0], color='white', linewidth=2)
ax.plot([60, 60], [0, 80], color='white', linewidth=1)
ax.plot([102, 102, 120, 120, 102], [18, 62, 62, 18, 18], color='white', linewidth=1)
ax.plot([0, 0, 18, 18, 0], [18, 62, 62, 18, 18], color='white', linewidth=1)
ax.plot([120, 120], [36, 44], color='white', linewidth=4)
ax.plot([0, 0], [36, 44], color='white', linewidth=4)

ax.set_xlim(0, 120)
ax.set_ylim(0, 80)
ax.axis('off')

plt.savefig('spain-euro-2024/pitch_blank.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.show()