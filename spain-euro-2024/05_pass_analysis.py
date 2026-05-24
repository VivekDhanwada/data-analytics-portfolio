import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"

MATCH_IDS = [3943043, 3942752, 3942226, 3941018, 3930179, 3930172, 3930160]
SPAIN_ID = 772

all_passes = []

for match_id in MATCH_IDS:
    events_url = f"{BASE_URL}/events/{match_id}.json"
    response = requests.get(events_url)
    events = response.json()
    
    for event in events:
        if event['type']['name'] == 'Pass' and event['team']['id'] == SPAIN_ID:
            event['match_id'] = match_id
            all_passes.append(event)

print(f"Total Spain Passes: {len(all_passes)}") 

print(json.dumps(all_passes[0], indent=2, ensure_ascii=False))

passer_data = []
for p in all_passes:
    if 'recipient' not in p['pass']:
        continue
    passer_data.append({
        'passer': p['player']['name'],
        'recipient': p['pass']['recipient']['name'],
        'x': p['location'][0],
        'y': p['location'][1],
        'match_id': p['match_id']
    })

df_passes = pd.DataFrame(passer_data)
print(df_passes.head())

df_passes.to_csv('spain-euro-2024/spain_passes.csv', index=False)
print("Saved: spain_passes.csv")

player_positions = df_passes.groupby('passer')[['x', 'y']].mean()
print(player_positions)

pass_combinations = df_passes.groupby(['passer', 'recipient']).size().reset_index(name='count')
print(pass_combinations.sort_values('count', ascending=False).head(10))

pass_counts = df_passes.groupby('passer').size()

strong_connections = pass_combinations[pass_combinations['count'] >= 35]
top_players = pass_counts.sort_values(ascending=False).head(11).index
print(f"Strong connections: {len(strong_connections)}")
print(f"Top Players: {(top_players)}")

nicknames = {
    'Rodrigo Hernández Cascante': 'Rodri',
    'Daniel Olmo Carvajal': 'Dani Olmo',
    'Álvaro Borja Morata Martín': 'Morata',
    'Lamine Yamal Nasraoui Ebana': 'Yamal',
    'Nicholas Williams Arthuer': 'Nico Williams',
    'Marc Cucurella Saseta': 'Cucurella',
    'Fabián Ruiz Peña': 'Fabián',
    'Daniel Carvajal Ramos': 'Carvajal',
    'Aymeric Laporte': 'Laporte',
    'Robin Aime Robert Le Normand': 'Le Normand',
    'Unai Simón Mendibil': 'Unai Simón',
    'José Ignacio Fernández Iglesias': 'Joselu',
    'Pedro González López': 'Pedri',
    'Mikel Oyarzabal Ugarte': 'Oyarzabal',
    'Martín Zubimendi Ibáñez': 'Zubimendi',
    'Mikel Merino Zazón': 'Merino',
    'Alejandro Grimaldo García': 'Grimaldo',
    'David Raya Martin': 'Raya',
    'José Luis Sanmartín Mato': 'Joselu',
    'Ferrán Torres García': 'Ferran Torres',
    'Jesús Navas González': 'Navas',
    'Fermin Lopez Marin': 'Fermín',
    'Alejandro Baena Rodríguez': 'Álex Baena',
    'Ayoze Pérez Gutiérrez': 'Ayoze',
    'Daniel Vivian Moreno': 'Vivian'
}

strong_connections = pass_combinations[pass_combinations['count'] >= 35]
top_players = pass_counts.sort_values(ascending=False).head(11).index
max_count = strong_connections['count'].max()

fig, ax = plt.subplots(figsize=(12, 8))

ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#1a1a2e')

ax.plot([0, 0, 120, 120, 0], [0, 80, 80, 0, 0], color='white', linewidth=2)
ax.plot([60, 60], [0, 80], color='white', linewidth=1)
ax.plot([102, 102, 120, 120, 102], [18, 62, 62, 18, 18], color='white', linewidth=1)
ax.plot([0, 0, 18, 18, 0], [18, 62, 62, 18, 18], color='white', linewidth=1)
ax.plot([120, 120], [36, 44], color='white', linewidth=4)
ax.plot([0, 0], [36, 44], color='white', linewidth=4)

for _, row in strong_connections.iterrows():
    if row['passer'] in player_positions.index and row['recipient'] in player_positions.index:
        x1, y1 = player_positions.loc[row['passer']]
        x2, y2 = player_positions.loc[row['recipient']]
        width = 1 + (row['count'] / max_count) * 4
        ax.plot([x1, x2], [y1, y2], color='#55DDE0', linewidth=width, alpha=0.55, zorder=1)

for player, row in player_positions.iterrows():
    if player not in top_players:
        continue
    size = 80 + pass_counts.get(player, 10) * 1.2
    ax.scatter(row['x'], row['y'], c='#F5A623', s=size, edgecolors='white', linewidth=0.8, zorder=5)
    label = nicknames.get(player, player.split()[0])
    ax.text(row['x'], row['y'] + 3, label, color='white', fontsize=8, ha='center')

ax.set_title(
    'Spain Euro 2024 — Passing Network\nNode size = passes made | Line width = pass frequency',
    color='white', fontsize=14, pad=15
)
ax.set_xlim(0, 120)
ax.set_ylim(0, 80)
ax.axis('off')

plt.savefig('spain-euro-2024/spain_passing_network.png', dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
plt.show()