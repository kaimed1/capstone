import csv
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Global Variables
input_schedule = '../data/Schedule.csv'
output_schedule = '../data/Training_Schedule_RF1.csv'

# Function for inital restructing of the schedule data
def format_schedule_data(input_schedule, output_schedule):
    print("Performing an initial restructuring of the data...")
    teams = []
    current_team = None
    current_conference = None

    with open(input_schedule, 'r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            # Skip empty lines and lines with only commas
            if not row or row == [',,,,,,']:
                continue

            # Check for data lines (assuming they start with '0')
            if row[0].isdigit() and row[0] == '0':
                if current_team is not None:
                    # Add columns: team name, conference, and data columns
                    date = row[1]
                    day = row[2]
                    location = row[3]
                    opponent = row[4]
                    result = row[5]
                    team_score = row[6]
                    opp_score = row[7]
                    new_row = [current_team, current_conference, date, day,
                               location, opponent, result, team_score, opp_score]
                    teams.append(new_row)
            else:
                current_team = row[0]
                current_conference = row[1]

    # Write the restructured data to a new CSV file
    with open(output_schedule, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header (add columns for team name, conference, and data)
        writer.writerow(['Team', 'Conference', 'Date', 'Day', 'Location',
                        'Opponent', 'Result', 'Score', 'Opponent Score'])
        # Write the rows
        writer.writerows(teams)


# Format Dataframe
def format_dataframe(df):
    print("Formatting the dates...")
    # Reformat date
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    print("Sorting by team and date...")
    # Sort by team, date
    df = df.sort_values(['Team', 'Date'])

    return df

# Change 'location' to 'Home' or 'Away'
def format_location(df):
    print("Formatting location...")
    df['Location'] = df['Location'].apply(lambda x: 'Home' if x == 'vs.' else 'Away')

    return df

# Calculate the running average score
def calc_running_avg_score(df):
    print("Calculating running average score...")
    df['Score'] = df['Score'].astype(int)
    df['RunningAvgScore'] = df.groupby('Team')['Score'].transform(lambda x: x.expanding().mean())

    return df


# Calculate the win rate for each team
def calc_win_rate(df):
    print("Calculating win rate...")
    df['Home_Win_Rate'] = df[df['Location'] == 'Home'].groupby(
        'Team')['Result'].transform(lambda x: x.eq('W').cumsum() / x.expanding().count())      
    df['Away_Win_Rate'] = df[df['Location'] == 'Away'].groupby(
        'Team')['Result'].transform(lambda x: x.eq('W').cumsum() / x.expanding().count())
    
    # Forward fill the win rates to fill NaN values
    df['Home_Win_Rate'] = df.groupby('Team')['Home_Win_Rate'].ffill()
    df['Away_Win_Rate'] = df.groupby('Team')['Away_Win_Rate'].ffill()
    
    # Backward fill the win rates to fill NaN values at the beginning
    df['Home_Win_Rate'] = df.groupby('Team')['Home_Win_Rate'].bfill()
    df['Away_Win_Rate'] = df.groupby('Team')['Away_Win_Rate'].bfill()

    return df


# Calculate the running total of wins/losses
def calc_win_loss(df):
    print("Calculating running total of wins and losses...")
    df['Wins'] = df.groupby('Team')['Result'].transform(
        lambda x: x.eq('W').cumsum())
    df['Losses'] = df.groupby('Team')['Result'].transform(
        lambda x: x.eq('L').cumsum())
    
    return df

# Calculate Bye Weeks
def calculate_bye_weeks(df):
    print("Calculating bye weeks...")
    # Initialize 'PrevWeekBYE' column with False
    df['PrevWeekBYE'] = 0

    # Iterate over each team individually
    for team, group in df.groupby('Team'):

        # Track whether the previous week was a bye
        prev_week_bye = 0

        # Group by week starting on Saturday and iterate
        prev_week = None

        for week_start, week_data in group.groupby(pd.Grouper(key='Date', freq='W-SAT')):
            if prev_week is not None:
                # Check if the previous week was a bye
                if (prev_week['Location'] == 'BYE').all():
                    prev_week_bye = 1
                else:
                    prev_week_bye = 0

                # Update the 'PrevWeekBYE' column for the current week
                df.loc[week_data.index, 'PrevWeekBYE'] = prev_week_bye

            # Update previous week info
            prev_week = week_data

    print("Removing bye weeks and extra days...")
    # Remove any rows with 'BYE' in the 'Location' column
    df = df[df['Location'] != 'BYE']

    return df

# Calculate and merge opponent stats
def calc_opponent_stats(df):
    print("Merging opponent stats...")
    # Rename columns to reflect opponent stats and avoid any naming conflicts
    opponent_df = df.rename(columns={
        'Team': 'Opponent_Team',  # Rename 'Team' to 'Opponent_Team'
        'RunningAvgScore': 'Opponent_RunningAvgScore',
        'Wins': 'Opponent_Wins',
        'Losses': 'Opponent_Losses',
        'Home_Win_Rate': 'Opponent_Home_Win_Rate',
        'Away_Win_Rate': 'Opponent_Away_Win_Rate',
    })

    # Drop unnecessary columns to avoid duplication (especially the original 'Opponent' column)
    opponent_df = opponent_df[['Opponent_Team', 'Date',
                            'Opponent_RunningAvgScore', 'Opponent_Wins',
                            'Opponent_Losses', 'Opponent_Home_Win_Rate',
                            'Opponent_Away_Win_Rate']]


    # Merge the opponent data back into the main DataFrame
    merged_df = pd.merge(df, opponent_df, how='left',
                        left_on=['Opponent', 'Date'],
                        right_on=['Opponent_Team', 'Date'])

    # Drop the 'Opponent_Team' column since it's redundant
    merged_df = merged_df.drop('Opponent_Team', axis=1)

    # Backfill the opponent stats to fill NaN values
    opponent_stats = ['Opponent_RunningAvgScore', 'Opponent_Wins', 'Opponent_Losses',
                    'Opponent_Home_Win_Rate', 'Opponent_Away_Win_Rate']
    merged_df[opponent_stats] = merged_df.groupby('Team')[opponent_stats].bfill()

    # Forward fill the opponent stats to fill NaN values at the beginning
    merged_df[opponent_stats] = merged_df.groupby('Team')[opponent_stats].ffill()

    # Reorder columns for better readability
    merged_df = merged_df[['Date', 'Day', 'Location', 'Conference', 'Team', 'PrevWeekBYE', 'RunningAvgScore', 'Wins', 'Losses',
                        'Home_Win_Rate', 'Away_Win_Rate', 'Opponent', 'Opponent_RunningAvgScore', 'Opponent_Wins', 'Opponent_Losses',
                        'Opponent_Home_Win_Rate', 'Opponent_Away_Win_Rate', 'Result', 'Score', 'Opponent Score']]

    # Fill any remaining NaN values with 0 for good measure
    merged_df.fillna(0, inplace=True)

    return merged_df

# Save df to a csv
def save_df(df):
    print("Data created successfully! Saving to " + output_schedule)
    df.to_csv(output_schedule)

# Calculate data from original schedule
# IMPORTANT: These functions must be called in this order
def calc_schedule_data(df):
    df = format_dataframe(df)
    df = calculate_bye_weeks(df)
    df = format_location(df)
    df = calc_running_avg_score(df)
    df = calc_win_loss(df)
    df = calc_win_rate(df)
    df = calc_opponent_stats(df)

    return df

def create_new_training_dataset():
    format_schedule_data(input_schedule, output_schedule)
    df = pd.read_csv(output_schedule)
    df = calc_schedule_data(df)

    # Select only numerical columns
    numerical_df = df.select_dtypes(include=['float64', 'int64'])

    # Calculate the correlation matrix
    corr_matrix = numerical_df.corr()

    # Set up the matplotlib figure
    plt.figure(figsize=(10, 8))

    # Create a heatmap with seaborn
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')

    # Display the heatmap
    plt.title("Feature Correlation Heatmap - RF1")
    plt.savefig('../data/correlation_heatmap_rf1.png')

    save_df(df)

def main():
    create_new_training_dataset()
    

if __name__ == "__main__":
    main()