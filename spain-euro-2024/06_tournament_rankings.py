import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


COMPETITION_ID = 55
SEASON_ID = 282
BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

matches_url = f"{BASE_URL}/matches/{COMPETITION_ID}/{SEASON_ID}.json"
response = requests.get(matches_url)
all_matches = response.json()

print(f"Total matches: {len(all_matches)}")

team_stats = {}

for match in all_matches:
    match_id = match['match_id']
    events_url = f"{BASE_URL}/events/{match_id}.json"
    response = requests.get(events_url)
    events = response.json()
    
    for event in events:
        team = event['team']['name']
        event_type = event['type']['name']
        
        if team not in team_stats:
            team_stats[team] = {'goals': 0, 'passes': 0, 'pressures': 0, 'recoveries': 0}
        
        if event_type == 'Shot' and event.get('shot', {}).get('outcome', {}).get('name') == 'Goal':
            team_stats[team]['goals'] += 1
        elif event_type == 'Pass':
            team_stats[team]['passes'] += 1
        elif event_type == 'Pressure':
            team_stats[team]['pressures'] += 1
        elif event_type == 'Ball Recovery':
            team_stats[team]['recoveries'] += 1

print("Done fetching all matches")

df_rankings = pd.DataFrame(team_stats).T.reset_index()
df_rankings.columns = ['team', 'goals', 'passes', 'pressures', 'recoveries']

df_rankings = df_rankings.sort_values('goals', ascending=False)
df_rankings['goals_rank'] = df_rankings['goals'].rank(ascending=False).astype(int)
df_rankings['passes_rank'] = df_rankings['passes'].rank(ascending=False).astype(int)
df_rankings['pressures_rank'] = df_rankings['pressures'].rank(ascending=False).astype(int)
df_rankings['recoveries_rank'] = df_rankings['recoveries'].rank(ascending=False).astype(int)

print(df_rankings[df_rankings['team'] == 'Spain'])

print(df_rankings.head)

df_rankings.to_csv('spain-euro-2024/tournament_rankings.csv', index=False)
print("Saved: tournament_rankings.csv")