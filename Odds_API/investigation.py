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

selected_sport = 'americanfootball_nfl'

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

    active_sports_dump = json.dumps(active_sports_json, indent=4)
    odds_dump = json.dumps(odds_json, indent=4)

    for game in range(len(odds_json)):
        game_id = odds_json[game]['id']
        sport = odds_json[game]['sport_title']
        game_start_time = odds_json[game]['commence_time']
        home_team = odds_json[game]['home_team']
        away_team = odds_json[game]['away_team']

        list_bookmakers = odds_json[game]['bookmakers']
        bookmaker = list_bookmakers[0]['title']

        list_markets = list_bookmakers[0]['markets']
        market = list_markets[0]['key']

        list_outcomes = list_markets[0]['outcomes']
        team1_name = list_outcomes[0]['name']
        team1_odds = list_outcomes[0]['price']
        team2_name = list_outcomes[1]['name']
        team2_odds = list_outcomes[1]['price']
