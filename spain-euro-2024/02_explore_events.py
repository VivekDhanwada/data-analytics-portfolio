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