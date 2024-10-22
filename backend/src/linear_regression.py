import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def ReadAndFormatData(file_path):
    # Load the data
    df = pd.read_csv(file_path)

    # Split the data into features and target
    features = df.drop(columns=['game_id', 'Result'])
    target = df['Result']

    # Create feature differences between every two rows (team matchups)
    team_a_stats = features.iloc[::2].reset_index(drop=True)
    team_b_stats = features.iloc[1::2].reset_index(drop=True)
    diff_stats = team_a_stats - team_b_stats  # Calculate the stat differences

    # Corresponding outcomes for the matchups
    game_outcomes = target.iloc[::2].reset_index(drop=True)  # Only take every other outcome

    return diff_stats, game_outcomes


def TrainModel(diff_stats, game_outcomes):
    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(diff_stats, game_outcomes, test_size=0.2, random_state=23)

    # Train the linear regression model
    lin_reg_model = LinearRegression()
    lin_reg_model.fit(X_train, y_train)
    return lin_reg_model, X_test, y_test

def TestModel(lin_reg_model, X_test, y_test):
    # Make predictions
    y_pred_continuous = lin_reg_model.predict(X_test)  # Continuous predictions

    # Convert continuous predictions to binary (0 or 1)
    y_pred_binary = (y_pred_continuous > 0.5).astype(int)  # Thresholding at 0.5

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred_binary)
    print(f'Linear Regression Model Accuracy: {accuracy:.5f}')

def SaveModel(lin_reg_model):
    # Save the linear regression model using joblib
    model_filename = 'backend/data/trained_models/linear_regression_model.pkl'
    joblib.dump(lin_reg_model, model_filename)
    print(f'Model saved to {model_filename}')

def main():
    # Path to data to read in
    file_path = 'backend/data/Schedule_Stats.csv'

    # Preparing data for training
    stats, outcomes = ReadAndFormatData(file_path)

    # Train and save model and test data
    model, x, y = TrainModel(stats, outcomes)

    # Test and evaluate accuracy
    TestModel(model, x, y)

    # Save model via joblib
    SaveModel(model)

if __name__ == "__main__":
    main()