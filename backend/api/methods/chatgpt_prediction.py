import requests
from json import loads as json_loads
from dotenv import dotenv_values

# Load environment variables
config = dotenv_values("backend/.env")

# chatgpt prediction
def chatgpt_prediction(home_team_name, away_team_name):

    try:
        # Set up request body
        body = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": f"""If the {home_team_name} and {away_team_name} college football teams played a game, who would win and what would the scores be.
        Format the response as: {{
            "winner_name": winner_name,
            "loser_name": loser_name,
            "winner_score": winner_score,
            "loser_score": loser_score
        }}
        """}],
            "temperature": 0.7
        }

        # Set up request headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {config["OPENAI_API_KEY"]}'
        }

        # Make post request
        res = requests.post("https://api.openai.com/v1/chat/completions", json=body, headers=headers)

        # Get response body
        res_body = res.json()

        # response body has a 'choices' array that should have length 1
        if "choices" not in res_body or len(res_body["choices"]) < 1:
            raise Exception("Unable to retrieve chatgpt response")

        # Load the chatgpt response message string as json
        outcome_json = json_loads(res_body["choices"][0]["message"]["content"])

        # Make sure that chatgpt responsed with all the fields we need (winner_name, loser_name, winner_score, loser_score)
        if "winner_name" not in outcome_json or "loser_name" not in outcome_json or "winner_score" not in "winner_score" or "loser_score" not in outcome_json:
            raise Exception("Malformed response from chatgpt")

        # Extract values
        winner_name = outcome_json["winner_name"]
        loser_name = outcome_json["loser_name"]
        winner_score = outcome_json["winner_score"]
        loser_score = outcome_json["loser_score"]

        return winner_name, loser_name, winner_score, loser_score, None
    
    except Exception as e:
        print(e)
        return "", "", "", "", f"{e}"

