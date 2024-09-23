import json
import pandas as pd
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
                average_point_diff = round(total_point_diff / game_count, 1)


                record[1 - outcome.value] += 1
                
                table_data.append({
                    'Team Name': name,
                    'Conference': league,
                    'Date': date,
                    'Day of Week': day,
                    'Location': site,
                    'Opponent': opponent,
                    'Outcome': outcome.name,
                    'Points For': points_for,
                    'Points Against': points_against,
                    'Point Differential': point_diff,
                    'Total Points For': total_points_for,
                    'Total Points Against': total_points_against,
                    'Total Point Diff': total_point_diff,
                    'Average Points For': average_points_for,
                    'Average Points Against': average_points_against,
                    'Average Point Diff': average_point_diff,
                    'Record': record.copy()
                })

    # Create a DataFrame from the table data
    df = pd.DataFrame(table_data)

    # Print the table
    print(df)
    return df

def main():
    schedule_path = 'backend/data/OneTeam.json'
    GetSchedules(schedule_path)

if __name__ == "__main__":
    main()