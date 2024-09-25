import os
import pandas as pd
import sqlite3 as sql
from collections import defaultdict
from JSON_parser import GetSchedules
from JSON_parser import GetSite
from JSON_parser import Outcome
from JSON_parser import Site

def PredictByScoring(home_adv):
    schedule_path = 'backend/data/Schedule.json'
    schedules = GetSchedules(schedule_path)
    predictions = {'Correct': 0, 'Incorrect': 0, 'Skipped': 0, 'Undefined': 0}

    for row in schedules.itertuples():
        team = row.Team_Name
        team_ppg = row.Previous_Average_Point_Diff
        
        opponent = row.Opponent
        opponent_ppg = GetPPG(opponent, team)

        site = Site[row.Location]
        outcome = Outcome[row.Outcome]

        if opponent_ppg == None:
            predictions['Skipped'] += 1
            continue

        if site == Site.Home:
            team_ppg += home_adv
        elif site == Site.Away:
            opponent_ppg += home_adv

        prediction = Outcome.InvalidOutcome
        if team_ppg > opponent_ppg:
            prediction = Outcome.W
        elif team_ppg < opponent_ppg:
            prediction = Outcome.L
        else:
            if site == Site.Home:
                prediction = Outcome.W
            elif site == Site.Away:
                prediction = Outcome.L
            else:
                predictions['Undefined'] += 1
                prediction = Outcome.L

        if outcome == prediction:
            predictions['Correct'] += 1
        else:
            predictions['Incorrect'] += 1

    return predictions

def GetPPG(team, opponent):
    db_path = 'backend/data/schedules.db'
    
    conn = sql.connect(db_path)
    cursor = conn.cursor()
    
    query = '''
    SELECT Previous_Average_Point_Diff
    FROM teams
    WHERE Team_Name = ? AND Opponent = ?
    '''
    
    cursor.execute(query, (team, opponent))
    
    result = cursor.fetchone()
    
    conn.close()

    if result and result[0] is not None:
        return result[0]
    else:
        return None

def main():
    predictions = PredictByScoring(5)
    # print(predictions)
    accuracy = (predictions['Correct'] * 100) / (predictions['Correct'] + predictions['Incorrect'])
    print(f"{accuracy:.3f}%")

if __name__ == "__main__":
    main()