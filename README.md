# Capstone- D1 Football Predictor

## Running Application

### 1. Make sure that JavaScript is installed, if not install here: https://nodejs.org/en
### 2. Download the frontend folder from this github repository
### 3. Navigate to the folder where app.js is located through the administrator version of command line
### 4. Run "npm install" to install all neccessary dependencies 
### 5. Lastly, type "npm start" in the command line and the application should open up a browser automatically at "http://localhost:3000/"

## Predicting a Game with Baseline Random Forest Model
An example of this can be seen in 'prediction_example_rf1.py', but the general steps are outlined below:

1. Create a CSV file with the same headers as seen in 'example_live_data.csv' (this will be automated later)
2. Load the CSV file into a pandas dataframe as well as the model and encoders .pkl files (use joblib)
3. Encode the categorical variables and define the features as seen below
```python
le_team = encoders['Team']
le_opponent = encoders['Opponent']
le_location = encoders['Location']
le_result = encoders['Result']

# Step 4: Encode categorical variables
df['Team_encoded'] = le_team.transform(df['Team'])
df['Opponent_encoded'] = le_opponent.transform(df['Opponent'])
df['Location_encoded'] = le_location.transform(df['Location'])

features = ['Team_encoded', 
                    'Location_encoded', 
                    'Opponent_encoded', 
                    'PrevWeekBYE', 
                    'Wins', 
                    'Losses', 
                    'RunningAvgScore', 
                    'Home_Win_Rate',
                    'Away_Win_Rate', 
                    'Opponent_Wins', 
                    'Opponent_Losses']
```
4. Call the prediction method on the model ensuring you pass in the dataframe 

## Where did the training data come from?
Initially we had a CSV file of all of last years games which included data stuch as the scores for each team, the result of the game, the location, etc. We took this data, reformatted it and derived some more data, and then saved that as a new CSV named 'Training_Schedule_RF1.csv'. Below is a general outline of how the data was restructured and what data was derived:

1. Initially, the CSV was read in to a pandas dataframe. This was tricky as the format of the data was a bit weird, so we had to check each line to ensure it was a line that contained data or if it was a new header line.
2. The date was changed to a pandas datetime type and the dataframe was sorted by team and date.
3. The location was reformatted in such a way that if it was originally 'vs.' it would now read as 'Home' for the first team listed, and if it said '@' it would read as 'Away'.
4. The running average score for each team during each week was calculated using a pandas transform function.
5. The win rate for each team was calculated for both home and away and then the dataframe was forward and backward filled with '0' values to fill any remaining NaN values due to lack of games.
6. The running total of win/losses was calculated for each team once again using a transform function.
7. For each game, we calculated whether the previous week was a bye week. Essentially if the previous week was full of 'BYE' for the location, then the new column would be set as '1', otherwise it is set as '0' if there was a game for that team in the previous week. Then all rows for bye games were removed to avoid a large amount of 'empty' rows (rows where there simply wasn't a game).
8. Each game was merged into a singular row such that it displayed both the home team and the away team as well as their respective stats rather than storing each game separated across 2 rows. 

This new training data set was saved to a new CSV where the headers are now ',Date,Day,Location,Conference,Team,PrevWeekBYE,RunningAvgScore,Wins,Losses,Home_Win_Rate,Away_Win_Rate,Opponent,Opponent_RunningAvgScore,Opponent_Wins,Opponent_Losses,Opponent_Home_Win_Rate,Opponent_Away_Win_Rate,Result,Score,Opponent Score' where the first column is a unique ID (this is not necessary now, but may be helpful later).

