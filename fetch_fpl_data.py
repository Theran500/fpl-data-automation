import requests
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

# Merge the players and teams data on the team ID
combined_df = pd.merge(players_df, teams_df, left_on='team', right_on='id', suffixes=('_player', '_team'))

# Merge with element types to include position data
combined_df = pd.merge(combined_df, element_types_df, left_on='element_type', right_on='id', suffixes=('', '_element_type'))

# To track gameweek performances, we typically need individual player performance data per gameweek.
# For the sake of simplicity, we assume you have a way to retrieve player performances per gameweek 
# from the 'https://fantasy.premierleague.com/api/event/{gameweek}/live/' endpoint.

# Example pseudo-code to show integration (this part needs a loop through gameweeks):
for event in events_df['id']:  # Loop through each gameweek ID
    gw_url = f"https://fantasy.premierleague.com/api/event/{event}/live/"
    gw_response = requests.get(gw_url)
    gw_data = gw_response.json()
    
    # Assuming gw_data['elements'] contains performance stats for all players
    gw_df = pd.json_normalize(gw_data['elements'])
    
    # Merge the gameweek performance data with the combined dataframe
    combined_df = pd.merge(combined_df, gw_df, left_on='id_player', right_on='id', suffixes=('', f'_GW{event}'))

# Save the combined DataFrame to a CSV file
combined_df.to_csv('fpl_combined_gameweeks.csv', index=False)

print("Data fetched and saved as fpl_combined_gameweeks.csv")