import json
import pandas as pd
import sqlite3 as sql
from enum import Enum

Site = Enum('Site', ['Home', 'Away', 'Neutral', 'InvalidSite'], start=0)

DayOfWeek = Enum('DayOfWeek', ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'InvalidDay'], start=0)

Outcome = Enum('Outcome', ['L', 'W', 'InvalidOutcome'], start=0)

def GetSite(site):
    ret = None
    
    if(site == 'vs.'):
        ret = Site.Home
    elif(site == '@'):
        ret = Site.Away
    elif(site == 'N'):
        ret = Site.Neutral
    else:
        ret = Site.InvalidSite
    
    return ret.name

def GetDay(day):
    ret = None

    if(day == 'Sun'):
        ret = DayOfWeek.Sunday
    elif(day == 'Mon'):
        ret = DayOfWeek.Monday
    elif(day == 'Tue'):
        ret = DayOfWeek.Tuesday
    elif(day == 'Wed'):
        ret = DayOfWeek.Wednesday
    elif(day == 'Thu'):
        ret = DayOfWeek.Thursday
    elif(day == 'Fri'):
        ret = DayOfWeek.Friday
    elif(day == 'Sat'):
        ret = DayOfWeek.Saturday
    else:
        ret = DayOfWeek.InvalidDay

    return ret.name

def GetOutcome(outcome):
    ret = None

    if(outcome == 'L'):
        ret = Outcome.L
    elif(outcome == 'W'):
        ret = Outcome.W
    else:
        ret = Outcome.InvalidOutcome

    return ret

def GetConferenceName(conference):
    str = ' Conference'
    if(conference.endswith(str)):
        return conference[:-len(str)]
    return conference

def GetSchedules(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    table_data = []

    for team in data['teams']:
        name = team['name']
        league = GetConferenceName(team['league'])
        record = [0,0]
        game_count = 0
        total_points_for = 0
        total_points_against = 0
        total_point_diff = 0
        average_point_diff = 0
        wins = 0
        losses = 0

        for i, game in enumerate(team['schedule']):
            if game['location'] != 'BYE':
                game_count += 1

                date = game['timestamp']
                day = GetDay(game['dayOfWeek'])
                site = GetSite(game['location'])
                opponent = game['opponent']
                outcome = GetOutcome(game['outcome'])
                points_for = int(game['pointsScored'])
                points_against = int(game['pointsAllowed'])
                point_diff = points_for - points_against
                total_points_for += points_for
                total_points_against += points_against
                total_point_diff = point_diff
                average_points_for = round(total_points_for / game_count, 1)
                average_points_against = round(total_points_against / game_count, 1)
                previous_diff = average_point_diff
                average_point_diff = round(total_point_diff / game_count, 1)
                if outcome == Outcome.W:
                    wins += 1
                else:
                    losses += 1
                
                table_data.append({
                    'Team_Name': name,
                    'Conference': league,
                    'Date': date,
                    'Day_of_Week': day,
                    'Location': site,
                    'Opponent': opponent,
                    'Outcome': outcome.name,
                    'Points_For': points_for,
                    'Points_Against': points_against,
                    'Point_Differential': point_diff,
                    'Total_Points_For': total_points_for,
                    'Total_Points_Against': total_points_against,
                    'Total_Point_Diff': total_point_diff,
                    'Average_Points_For': average_points_for,
                    'Average_Points_Against': average_points_against,
                    'Previous_Average_Point_Diff': previous_diff,
                    'New_Average_Point_Diff': average_point_diff,
                    'Wins': wins,
                    'Losses': losses
                })

    # Create a DataFrame from the table data
    df = pd.DataFrame(table_data)

    # Print the table
    #print(df)
    return df

def main():
    conn = sql.connect('backend/data/schedules.db')
    
    schedule_path = 'backend/data/Schedule.json'
    
    scheudles = GetSchedules(schedule_path)

    scheudles.to_sql('teams', conn, if_exists='replace', index=False)

    conn.close()

if __name__ == "__main__":
    main()