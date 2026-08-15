import pandas as pd
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client['Assignment1']
source_col = db['Data_clean']
target_col = db['coffee_extracted']
target_col.delete_many({})

df = pd.read_csv('coffee_sales.csv')
df.dropna(inplace=True)
df = df[df['cash_type'] == 'card']

with open('task1_1_output.txt', 'w') as file:
    for _, row in df.iterrows():
        timestamp = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S.%f')
        triplet = {
            "coffee_type": row['coffee_name'],
            "user_id": row['card'],
            "money": row['money'],
            "day": timestamp.day,
            "month": timestamp.month,
            "year": timestamp.year,
            "time": timestamp.strftime('%H:%M:%S')
        }
        file.write(f"{triplet}\n")
        target_col.insert_one(triplet)

print("task1_1 completed: Output saved to task1_1_output.txt and inserted into MongoDB.")
