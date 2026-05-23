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