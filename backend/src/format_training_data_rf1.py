import csv
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Global Variables
input_schedule = '../data/Schedule.csv'
output_schedule = '../data/Training_Schedule_RF1.csv'

# Function for custom restructuring of the schedule data
def format_schedule_data(input_schedule, output_schedule):
    """
    This function reads the schedule data from the input CSV file, restructures it, and writes the 
    restructured data to a new CSV file to later be loaded into a DataFrame.

    Parameters:
    input_schedule (str): The path to the input CSV file containing the schedule data
    output_schedule (str): The path to the output CSV file to write the restructured data
    """
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

            # If the first column is a digit and equals '0', it indicates a game line
            if row[0].isdigit() and row[0] == '0':
                if current_team is not None:
                    # Parse game data
                    date = row[1]
                    day = row[2]
                    location = row[3]
                    opponent = row[4]
                    result = row[5]
                    team_score = row[6] if row[6] else 0
                    opp_score = row[7] if row[7] else 0
                    new_row = [current_team, current_conference, date, day, location, opponent, result, team_score, opp_score]
                    teams.append(new_row)
            else:
                # Parse team and conference names
                current_team = row[0]
                current_conference = row[1]

    # Write the restructured data to a new CSV file
    with open(output_schedule, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header (add columns for team name, conference, and data)
        writer.writerow(['Team', 'Conference', 'Date', 'Day', 'Location', 'Opponent', 'Result', 'Score', 'Opponent Score'])
        # Write the rows
        writer.writerows(teams)

# Format DataFrame
def format_dataframe(df):
    """
    This function formats the DataFrame by converting the date data type and sorting by team and date.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """
    print("Formatting the dates...")
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    # Drop Conference column
    df = df.drop('Conference', axis=1)

    print("Sorting by team and date...")
    df = df.sort_values(['Team', 'Date'])

    return df

# Change 'location' to 'Home' or 'Away'
def format_location(df):
    """
    This function formats the 'Location' column to 'Home' or 'Away'.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """
    print("Formatting location...")
    df['Location'] = df['Location'].apply(lambda x: 'Home' if x == 'vs.' else 'Away')

    return df

# Calculate the running average score
def calc_running_avg_score(df):
    """
    This function calculates the running average score for each team.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """
    print("Calculating running average score...")
    df['Score'] = df['Score'].astype(int)
    df['RunningAvgScore'] = df.groupby('Team')['Score'].transform(lambda x: x.expanding().mean())

    return df


# Calculate the win rate for each team
def calc_win_rate(df):
    """
    This function calculates the win rate for each team.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """
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
    """
    This function calculates the running total of wins and losses for each team.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """
    print("Calculating running total of wins and losses...")
    df['Wins'] = df.groupby('Team')['Result'].transform(
        lambda x: x.eq('W').cumsum())
    df['Losses'] = df.groupby('Team')['Result'].transform(
        lambda x: x.eq('L').cumsum())
    
    return df

# Calculate Bye Weeks
def calculate_bye_weeks(df):
    """
    This function calculates a new column 'PrevWeekBye" for each team which identifies if the previous week was a 
    bye week or notand removes entries with 'BYE' in the 'Location' column.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """
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

    # Drop Day
    df = df.drop('Day', axis=1)

    return df

# Calculate and merge opponent stats
def calc_opponent_stats(df):
    """
    This function merges the 2 rows for each game into 1 row where both the team and opponent stats are present.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """

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

    for team, group in df.groupby('Team'):
        prev_week_bye = 0  # Track if the previous week was a bye
        prev_week = None

        for week_start, week_data in group.groupby(pd.Grouper(key='Date', freq='W-SAT')):
            if prev_week is not None:
                if (prev_week['Location'] == 'BYE').all():
                    prev_week_bye = 1
                else:
                    prev_week_bye = 0
                # Update 'PrevWeekBYE' for the current week
                df.loc[week_data.index, 'PrevWeekBYE'] = prev_week_bye
            prev_week = week_data

    return df

# Transform 'Location' to binary HomeTeamAdvantage
def format_location(df):
    print("Formatting location to HomeTeamAdvantage...")
    df['HomeTeamAdvantage'] = df['Location'].apply(lambda x: 1 if x == 'vs.' else 0)
    df = df.drop('Location', axis=1)  # Remove the original 'Location' column
    return df

# Calculate running average score for each team
def calc_running_avg_score(df):
    print("Calculating running average score...")
    df['Score'] = df['Score'].astype(int)
    df['RunningAvgScore'] = df.groupby('Team')['Score'].transform(lambda x: x.expanding().mean())
    return df

# Calculate win rate for home and away games
def calc_win_rate(df, separate_home_away=True):
    print("Calculating win rates...")
    if separate_home_away:
        # Calculate win rate for home and away games
        df['Home_Win_Rate'] = df[df['HomeTeamAdvantage'] == 1].groupby('Team')['Result'].transform(lambda x: x.eq('W').cumsum() / x.expanding().count())
        df['Away_Win_Rate'] = df[df['HomeTeamAdvantage'] == 0].groupby('Team')['Result'].transform(lambda x: x.eq('W').cumsum() / x.expanding().count())
        # Fill NaN values forward and backward
        df['Home_Win_Rate'] = df.groupby('Team')['Home_Win_Rate'].ffill().bfill()
        df['Away_Win_Rate'] = df.groupby('Team')['Away_Win_Rate'].ffill().bfill()
    else:
        # Calculate a single win rate
        df['Win_Rate'] = df.groupby('Team')['Result'].transform(lambda x: x.eq('W').cumsum() / x.expanding().count())
        # Fill NaN values
        df['Win_Rate'] = df.groupby('Team')['Win_Rate'].ffill().bfill()

    return df

# Calculate running total of wins and losses for each team
def calc_win_loss(df):
    print("Calculating running total of wins and losses...")
    df['Wins'] = df.groupby('Team')['Result'].transform(lambda x: x.eq('W').cumsum())
    df['Losses'] = df.groupby('Team')['Result'].transform(lambda x: x.eq('L').cumsum())
    return df

# Save df to a csv
def save_df(df):
    """
    This function saves the DataFrame to a CSV file.

    Parameters:
    df (DataFrame): The DataFrame containing the schedule data
    """

    print("Data created successfully! Saving to " + output_schedule)
    df.to_csv(output_schedule)

# Calculate data from original schedule
# IMPORTANT: These functions must be called in this order
def calc_schedule_data(df):
    """
    This function calls the functions to calculate the new features for the schedule data. It is IMPORTANT that these functions
    are called in this order to ensure data is calculated correctly.
    """
    df = format_dataframe(df)
    df = remove_bye_weeks_and_extra_days(df)  # Remove bye weeks and extra days
    df = calculate_bye_weeks(df)  # Add the 'PrevWeekBYE' column
    df = format_location(df)
    df = calc_running_avg_score(df)
    df = calc_win_loss(df)
    df = calc_win_rate(df, separate_home_away=separate_home_away)
    return df

def create_new_training_dataset():
    """ 
    This function creates a new training dataset for the Random Forest model by reading the schedule data, formatting it and
    calculating new features. It then creates a correlation matrix heatmap to visualize the relationships between the features
    and then saves the new dataset to a CSV file.
    """
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
    # Set 'separate_home_away' to False if you want a single running win rate
    create_new_training_dataset(separate_home_away=True)

if __name__ == "__main__":
    main()
