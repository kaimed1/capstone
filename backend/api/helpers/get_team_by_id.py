from django.db import connection


def get_team_by_id(id):
    try:
        cursor = connection.cursor()

        # Query teams by id
        cursor.execute(f'SELECT Team FROM teams WHERE team_id = {int(id)}')

        # Get the actual rows
        teams = cursor.fetchall()

        # If length of teams < 1, team wasn't found
        if len(teams) < 1:
            return None

        return teams[0][0]
    except:
        print('Unable to fetch team from teams table')
        return None