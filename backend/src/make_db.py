import json
import pandas as pd
import sqlite3 as sql

# Connect to the database (creates it if it doesn't exist)
conn = sql.connect('../data/football.db') 

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        TeamID INTEGER PRIMARY KEY,
        TeamName TEXT NOT NULL
    )
''')

# Commit the changes
conn.commit()



# Load Teams data
teams = pd.read_csv('../data/Teams.csv')
teams.to_sql('teams', conn, if_exists='replace', index=False)

# Print the first 5 rows of the table
cursor.execute('SELECT * FROM teams LIMIT 5')

# Fetch the results
results = cursor.fetchall()
print(results)


# Close the connection
conn.close()