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

# Fetch fixtures data (match details)
fixtures_url = "https://fantasy.premierleague.com/api/fixtures/"
fixtures_response = requests.get(fixtures_url)
fixtures_data = fixtures_response.json()
fixtures_df = pd.json_normalize(fixtures_data)

# Merge the players and teams data on the team ID
combined_df = pd.merge(players_df, teams_df, left_on='team', right_on='id', suffixes=('_player', '_team'))

# Merge with element types to include position data
combined_df = pd.merge(combined_df, element_types_df, left_on='element_type', right_on='id', suffixes=('', '_element_type'))

# To track gameweek performances, loop through each gameweek ID
for event in events_df['id']:  # Loop through each gameweek ID
    gw_url = f"https://fantasy.premierleague.com/api/event/{event}/live/"
    gw_response = requests.get(gw_url)
    gw_data = gw_response.json()
    
    # Assuming gw_data['elements'] contains performance stats for all players
    gw_df = pd.json_normalize(gw_data['elements'])
    
    # Merge the gameweek performance data with the combined dataframe
    combined_df = pd.merge(combined_df, gw_df, left_on='id_player', right_on='id', suffixes=('', f'_GW{event}'))

# Optional: Merge fixtures data if needed to include match details
# Merging fixtures data on home/away team ID
combined_df = pd.merge(combined_df, fixtures_df, left_on='team', right_on='team_h', how='left', suffixes=('', '_match_h'))
combined_df = pd.merge(combined_df, fixtures_df, left_on='team', right_on='team_a', how='left', suffixes=('', '_match_a'))

# Save the combined DataFrame to a CSV file
combined_df.to_csv('fpl_combined_with_matches.csv', index=False)

print("Data fetched and saved as fpl_combined_with_matches.csv")
