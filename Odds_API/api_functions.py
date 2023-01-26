import requests


def pull_active_sports(api):
    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports',
        params={
            'api_key': api
        }
    )

    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

    active_sports_json = sports_response.json()
    return active_sports_json


def pull_sport_odds(api_key, selected_sport, regions, markets, odds_format, date_format, bookmakers):
    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{selected_sport}/odds',
        params={
            'api_key': api_key,
            'regions': regions,
            'markets': markets,
            'oddsFormat': odds_format,
            'dateFormat': date_format,
            'bookmakers': bookmakers,
        })
    if odds_response.status_code != 200:
        print(f'Failed to get sports: status_code {odds_response.status_code}, response body {odds_response.text}')

    odds_json = odds_response.json()
    return odds_json

