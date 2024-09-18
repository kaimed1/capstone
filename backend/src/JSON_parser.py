import json
import pandas as pd
from enum import Enum

Site = Enum('Site', ['Home', 'Away', 'Neutral', 'InvalidSite'])

DayOfWeek = Enum('DayOfWeek', ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'InvalidDay'])

Outcome = Enum('Outcome', ['L', 'W', 'InvalidOutcome'])

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
    
    return ret

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

    return ret

def GetOutcome(outcome):
    ret = None

    if(outcome == 'L'):
        ret = Outcome.L
    elif(outcome == 'W'):
        ret = Outcome.W
    else:
        ret = Outcome.InvalidOutcome.name

    return ret

def getConferenceName(conference):
    str = ' Conference'
    if(conference.endswith(str)):
        return conference[:-len(str)]
    return conference

file_path = 'backend/data/Schedule.json'
with open(file_path, 'r') as file:
    data = json.load(file)

table_data = []

for team in data['teams']:
    name = team['name']
    league = getConferenceName(team['league'])
    
    
    for i, game in enumerate(team['schedule']):
        if game['location'] != 'BYE':
            table_data.append({
                'Team Name': name,
                'Conference': league,
                'Date': game['timestamp'],
                'Day of Week': GetDay(game['dayOfWeek']).name,
                'Location': GetSite(game['location']).name,
                'Opponent': game.get('opponent', ''),
                'Outcome': GetOutcome(game.get('outcome', '')).name,
                'Points For': game.get('pointsScored', ''),
                'Points Against': game.get('pointsAllowed', '')
            })

# Create a DataFrame from the table data
df = pd.DataFrame(table_data)

# Print the table
print(df)