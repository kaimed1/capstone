import joblib
import pandas as pd

# Load the model from the file
model = joblib.load('../data/trained_models/rf_model_1.pkl')

# Load the data
df = pd.read_csv('../data/example_live_data.csv')

# Load Encoders
encoders = joblib.load('../data/trained_models/encoders.pkl')
le_team = encoders['Team']
le_opponent = encoders['Opponent']
le_location = encoders['Location']
le_result = encoders['Result']

# Encode categorical variables
df['Team_encoded'] = le_team.transform(df['Team'])
df['Opponent_encoded'] = le_opponent.transform(df['Opponent'])
df['Location_encoded'] = le_location.transform(df['Location'])

# Define the features that will be used to make the predictions
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

# Make the prediction using the df and defined features
predictions = model.predict(df[features])

# Print the prediction
print(predictions)