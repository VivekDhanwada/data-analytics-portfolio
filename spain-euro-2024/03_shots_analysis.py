import requests
import json
import pandas as pd

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