import requests
import json
import pandas as pd

# Fetch data from the FPL API
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
response = requests.get(url)
data = response.json()

# Convert relevant parts of the data to DataFrames
players_df = pd.json_normalize(data['elements'])
teams_df = pd.json_normalize(data['teams'])
events_df = pd.json_normalize(data['events'])
element_types_df = pd.json_normalize(data['element_types'])
element_stats_df = pd.json_normalize(data['element_stats'])

# Save each DataFrame to a CSV file
players_df.to_csv('players.csv', index=False)
teams_df.to_csv('teams.csv', index=False)
events_df.to_csv('events.csv', index=False)
element_types_df.to_csv('element_types.csv', index=False)
element_stats_df.to_csv('element_stats.csv', index=False)

print("Data fetched and saved as CSV files:")
print(" - players.csv")
print(" - teams.csv")
print(" - events.csv")
print(" - element_types.csv")
print(" - element_stats.csv")
