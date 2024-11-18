# Returns a list of all the available prediction methods
def get_prediction_methods():
    return [
            {
            "name": "Flip a Coin",
            "description": "a random prediction that is not based on any statistics",
            "path": "api/random"
            },
            {
                "name": "ChatGPT Prediction",
                "description": "utilize ChatGPT to predict the outcome of a game",
                "path": "api/chatgpt"
            },
            {
                "name": "Random Forest Model",
                "description": "a random forest model trained on season long statistics",
                "path": "api/random_forest_2023"
            },
            {
                "name": "Decision Tree Model",
                "description": "a decision tree model trained on season long statistics",
                "path": "api/decision_tree"
            },
            {
                "name": "Linear Regression Model",
                "description": "a linear regression model trained on season long statistics",
                "path": "api/linear"
            },
            {
                "name": "Logistic Regression Model",
                "description": "a logistic regression model trained on season long statistics",
                "path": "api/logistic"
            }
        ]