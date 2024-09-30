import os
import pandas as pd
import sqlite3 as sql
from collections import defaultdict
from JSON_parser import GetSchedules
from JSON_parser import GetSite
from JSON_parser import Outcome
from JSON_parser import Site

def CheckAccuracy():
    schedule_path = 'backend/data/Schedule.json'
    schedules = GetSchedules(schedule_path)
    predictions = {'Correct': 0, 'Incorrect': 0, 'Skipped': 0}

    for row in schedules.itertuples():
        team = row.Team_Name        
        opponent = row.Opponent

        outcome = Outcome[row.Outcome]
        prediction = PredictMatchup(team, opponent)

        if outcome == Outcome.InvalidOutcome:
            predictions['Skipped'] += 1
        elif outcome == prediction:
            predictions['Correct'] += 1
        else:
            predictions['Incorrect'] += 1


    return predictions

def PredictMatchup(team, opponent):
    
    team_ppg = GetPPG(team)
    opponent_ppg = GetPPG(opponent)
    
    site = Site[GetSite(team, opponent)]

    prediction = Outcome.InvalidOutcome

    if opponent_ppg == None:
        return Outcome.W

    if site == Site.Home:
        team_ppg += 5
    elif site == Site.Away:
        opponent_ppg += 5

    if team_ppg > opponent_ppg:
        prediction = Outcome.W
    elif team_ppg < opponent_ppg:
        prediction = Outcome.L
    else:
        if site == Site.Home:
            prediction = Outcome.W
        else:
            prediction = Outcome.L


    return prediction

def GetSite(team, opponent):
    db_path = 'backend/data/schedules.db'
    
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    
    query = '''
    SELECT Location
    FROM teams
    WHERE Team_Name = ? AND Opponent = ?
    '''
    
    cursor.execute(query, (team, opponent))
    
    result = cursor.fetchone()
    
    conn.close()

    if result and result[0] is not None:
        return result[0]
    else:
        return Site.Home

def GetPPG(team):
    db_path = 'backend/data/schedules.db'
    
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    
    query = '''
    SELECT Average_Point_Diff
    FROM teams
    WHERE Team_Name = ? AND Game_Number = (SELECT MAX(Game_Number) FROM teams WHERE Team_Name = ?);
    '''
    
    cursor.execute(query, (team, team))
    
    result = cursor.fetchone()
    
    conn.close()

    if result and result[0] is not None:
        return result[0]
    else:
        return 0

def main():
    predictions = CheckAccuracy()
    print(predictions)
    accuracy = (predictions['Correct'] * 100) / (predictions['Correct'] + predictions['Incorrect'])
    print(f"{accuracy:.3f}%")
    print(PredictMatchup('Michigan State Spartans', 'Michigan Wolverines'))

if __name__ == "__main__":
    main()