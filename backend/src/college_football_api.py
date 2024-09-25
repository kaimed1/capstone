import requests
import json

base_url = "https://api.collegefootballdata.com"
access_token = "J+ypad8T6Z9Y2QI5eXgjrQRpm+lY1YgNblbS90ILIrz6P4WwsDHHyv3vAsZCdCtX"

headers = {
    "Authorization": f"Bearer {access_token}"
}


def get_teams():
    url = base_url + "/teams?conference=SEC"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        return data
    else:
        print(f"Error: {response.status_code}")

def get_stats():
    url = base_url + "/stats/season/advanced?year=2023"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Write data to a file
        with open('stats.json', 'w') as f:
            json.dump(response.json(), f)

    else:
        print(f"Error: {response.status_code}")

data = get_teams()

for team in data:
    print(team['school'] + " " + str(team['location']['grass']))

get_stats()

