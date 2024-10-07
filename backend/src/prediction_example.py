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

predictions = model.predict(df[features])

# Get each prediction and decode it being sure to take into account that is a multi-target model


# Print the predictions

print(predictions)
