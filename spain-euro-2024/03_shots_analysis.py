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
            all_shots.append(event)

print(f"Total Spain shots: {len(all_shots)}") 