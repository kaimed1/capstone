import csv
import pandas as pd
from datetime import datetime, timedelta

# Global Variables
input_schedule = '../data/Schedule.csv'
output_schedule = '../data/Training_Schdule.csv'
df = None

# Function for inital restructing of the schedule data
def format_schedule_data(input_schedule, output_schedule):
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
    # Reformat date
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # Sort by team, date
    df = df.sort_values(['Team', 'Date'])

    return df

# Change 'location' to 'Home' or 'Away'
def format_location(df):
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

# Save df to a csv
def save_df(df):
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

    return df

def create_new_training_dataset():
    global df
    format_schedule_data(input_schedule, output_schedule)
    df = pd.read_csv(output_schedule)
    df = calc_schedule_data(df)
    save_df(df)

def main():
    create_new_training_dataset()
    

if __name__=="__main__":
    main()

