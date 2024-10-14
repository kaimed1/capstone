import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

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

# Define the hyperparameters for the Random Forest model (these essentially define how the model will be trained)
rf_params = {
    'n_estimators': 200,
    'max_depth': 10,
    'min_samples_split': 10,
    'min_samples_leaf': 2,
    'bootstrap': True
}

def load_and_prepare_data(filepath):
    """
    This method loads the data from the given file, encodes the categorical columns, and returns the data and the encoders

    Parameters:
    filepath (str): The path to the CSV file containing the data
    """
    data = pd.read_csv(filepath)
    
    # Encode the categorical columns
    label_encoders = {}
    for column in ['Team', 'Opponent', 'Location', 'Result']:
        le = LabelEncoder()
        data[f'{column}_encoded'] = le.fit_transform(data[column].astype(str))
        label_encoders[column] = le

    return data, label_encoders

def train_rf_model(x_train, y_train, config):
    """
    This method trains a Random Forest model using the given training data and hyperparameters.

    Parameters:
    x_train (DataFrame): The training data
    y_train (DataFrame): The target labels
    config (dict): The hyperparameters for the Random Forest model
    """
    # Using a random state for reproducibility
    model = RandomForestClassifier(**config, random_state=42)
    model.fit(x_train, y_train)
    return model

def calc_accuracy(model, x, y):
    """
    This method calculates the accuracy of the model using cross-validation.

    Parameters:
    model (RandomForestClassifier): The trained Random Forest model
    x (DataFrame): The data to test the model on
    y (DataFrame): The target labels
    """
    scores = cross_val_score(model, x, y, cv=5)
    return scores.mean()

def find_best_parameters():
    """
    This method is used to find the best hyperparameters for the Random Forest model. It only needs to be run once,
    but I am keeping it here for reference. The best hyperparameters are then used to train the model are stored in
    the rf_params dictionary.
    """
    param_grid = {
            'n_estimators': [50, 100, 200, 250, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10, 15],
            'min_samples_leaf': [1, 2, 4, 8],
            'bootstrap': [True, False]
        }
    grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42),
                                param_grid=param_grid,
                                cv=5,
                                n_jobs=-1,
                                verbose=2)
    # Fit the model
    grid_search.fit(X_train, y_train)

    # Get the best hyperparameters
    best_params = grid_search.best_params_
    print(f"Best Hyperparameters: {best_params}")

def train_save_model():
    """
    This method loads the data, trains the Random Forest model, calculates the accuracy of the model, and saves the model.
    """
    global attribute_columns, rf_params
    data, encoders = load_and_prepare_data("../data/Training_Schedule_RF1.csv")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data[attribute_columns], data['Result_encoded'], test_size=0.3, random_state=42, stratify=data['Result_encoded'])

    # Train the Random Forest model
    rf_model = train_rf_model(X_train, y_train, rf_params)

    # Calculate the accuracy of the model
    accuracy = calc_accuracy(rf_model, X_train, y_train)
    print(f"Accuracy: {accuracy:.2f}")

    # Save the model and encoders
    joblib.dump(rf_model, '../data/trained_models/rf_model_1.pkl')
    joblib.dump(encoders, '../data/trained_models/encoders.pkl')

train_save_model()