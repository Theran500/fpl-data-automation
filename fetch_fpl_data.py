import requests
import json
import pandas as pd

# Example: Fetch Premier League players' data
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Convert relevant parts to DataFrame
players_df = pd.json_normalize(data['elements'])
players_df.to_csv('players.csv', index=False)

print("Data fetched and saved as players.csv")