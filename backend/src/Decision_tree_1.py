import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder

# Define the attribute columns that will be used to train the model
attribute_columns = ['Team_encoded',
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

# Configuration for the DecisionTree model
dt_params = {
    'max_depth': 20,
    'min_samples_split': 5,
}

# Define the hyperparameters for the Random Forest model
def load_and_prepare_data(filepath):
    """
    This method loads the data from the given file, encodes the categorical columns, and returns the data and the encoders variables

    Parameters:
    filepath (str): The path to the CSV file containing the data
    Returns: data and encoders formatted for the model to correctly read
    """
    data = pd.read_csv(filepath)

    # Encode the categorical columns
    label_encoders = {}
    for column in ['Team', 'Opponent', 'Location', 'Result']:
        le = LabelEncoder()
        data[f'{column}_encoded'] = le.fit_transform(data[column].astype(str))
        label_encoders[column] = le

    return data, label_encoders

def train_dt_model(x_train, y_train, config):
    """
    This method trains the Decision Tree using the given training data and hyperparameters.

    Parameters:
    x_train (DataFrame): The training data
    y_train (DataFrame): The target labels
    config (dict): The hyperparameters for the Decision Tree model
    Returns: The trained Decision Tree model
    """
    # Using a random state for reproducibility
    model = DecisionTreeClassifier(**config, random_state=42)
    model.fit(x_train, y_train)
    return model

def calc_accuracy(model, x, y):
    """
    This method calculates the accuracy of the model using cross-validation.

    Parameters:
    model (DecisionTreeClassifier): The trained Decision Tree model
    x (DataFrame): The data to test the model on
    y (DataFrame): The target labels
    Returns: The accuracy of the model
    """
    scores = cross_val_score(model, x, y, cv=5)
    return scores.mean()


def train_save_model():
    """
    This method loads the data, trains the Random Forest model, calculates the accuracy of the model, and saves the model.
    """
    #TODO: Need to change filename before put into git
    filepath = "Training_Schedule.csv"
    global attribute_columns
    data, encoders = load_and_prepare_data(filepath)

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(data[attribute_columns], data['Result_encoded'], test_size=0.3, random_state=42, stratify=data['Result_encoded'])

    # Train the Random Forest model
    dt_model = train_dt_model(x_train, y_train, dt_params)

    # Calculate the accuracy of the model
    accuracy = calc_accuracy(dt_model, x_train, y_train)
    print(f"Accuracy: {accuracy:.2f}")

    # Save the model and encoders
    #TODO: Need to change filename before put into git
    joblib.dump(dt_model, 'dt_model_1.pkl')
    joblib.dump(encoders, 'dt_encoders.pkl')

if __name__ == "__main__":
    train_save_model()