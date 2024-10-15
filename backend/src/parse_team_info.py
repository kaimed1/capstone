import pandas as pd

schedule_df = pd.read_csv("../data/Training_Schedule.csv")

# Extract the unique teams (assuming the CSV has columns like 'team_name' and 'conference')
teams_df = schedule_df[['Team', 'Conference']].drop_duplicates().reset_index(drop=True)

# Add a unique team_id (1 to N, where N is the number of teams)
teams_df['team_id'] = range(1, len(teams_df) + 1)

# Rearrange the columns if needed
teams_df = teams_df[['team_id', 'Team', 'Conference']]

# Save the new team CSV
teams_df.to_csv("../data/Teams.csv", index=False)

print(f"Team CSV generated and saved as Teams.csv")


