import os
from dotenv import load_dotenv
import json
import requests

# getting api key from environment
load_dotenv('api_key.env')
api_key = os.getenv('api_key')

# getting list of all in-season sports from API

sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports',
    params={
        'api_key': api_key
    }
)


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    print('List of in season sports:', sports_response.json())

selected_sport = 'americanfootball_ncaaf'

# getting list of all upcoming bets from selected sport from FanDuel Sportsbook

sport = 'upcoming'
regions = 'us'
markets = 'h2h'
odds_format = 'american'
date_format = 'iso'

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{selected_sport}/odds',
    params={
        'api_key': api_key,
        'regions': regions,
        'markets': markets,
        'oddsFormat': odds_format,
        'dateFormat': date_format,
        'bookmakers': 'fanduel'
    }
)


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    active_sports_json = sports_response.json()
    odds_json = odds_response.json()
    active_sports_json = json.dumps(active_sports_json, indent=4)
    odds_json = json.dumps(odds_json, indent=4)

print(1)
