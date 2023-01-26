import os
from dotenv import load_dotenv
import json
import pandas as pd
import api_functions as api

# creating a pandas db for the storage of game information
game_db = pd.DataFrame(columns=['GAME_ID', 'SPORT', 'START_TIME', 'HOME_TEAM', 'AWAY TEAM'])

wager_db = pd.DataFrame(columns=['GAME_ID', 'BOOKMAKER', 'WAGER_TYPE', 'HOME_TEAM_LINE', 'AWAY_TEAM_LINE'])

sports_db = pd.DataFrame(columns=[''])

# getting api key from environment
load_dotenv('api_key.env')
api_key = os.getenv('api_key')

# getting list of all in-season sports from API - serialize this list for categorization purposes
active_sports_json = api.pull_active_sports(api_key)

selected_sport = 'basketball_nba'
regions = 'us'
markets = 'h2h'
odds_format = 'american'
date_format = 'iso'
bookmakers = 'fanduel'

odds_json = api.pull_sport_odds(api_key, selected_sport, regions, markets, odds_format, date_format, bookmakers)

active_sports_dump = json.dumps(active_sports_json, indent=4)
odds_dump = json.dumps(odds_json, indent=4)

for game in range(len(odds_json)):
    game_id = odds_json[game]['id']
    sport = odds_json[game]['sport_title']
    game_start_time = odds_json[game]['commence_time']
    home_team = odds_json[game]['home_team']
    away_team = odds_json[game]['away_team']

    list_bookmakers = odds_json[game]['bookmakers']
    if not list_bookmakers:
        break
    bookmaker = list_bookmakers[0]['title']

    list_markets = list_bookmakers[0]['markets']
    market = list_markets[0]['key']

    list_outcomes = list_markets[0]['outcomes']
    team1_name = list_outcomes[0]['name']
    team1_odds = list_outcomes[0]['price']
    team2_name = list_outcomes[1]['name']
    team2_odds = list_outcomes[1]['price']

    if team1_name == home_team:
        home_team_odds = team1_odds
        away_team_odds = team2_odds
    else:
        away_team_odds = team1_odds
        home_team_odds = team2_odds

    game_db_upload = pd.DataFrame([[game_id, sport, game_start_time, home_team, away_team]],
                                  columns=['GAME_ID', 'SPORT', 'START_TIME', 'HOME_TEAM', 'AWAY TEAM'])
    wager_db_upload = pd.DataFrame([[game_id, bookmaker, market, home_team_odds, away_team_odds]],
                                   columns=['GAME_ID', 'BOOKMAKER', 'WAGER_TYPE', 'HOME_TEAM_LINE', 'AWAY_TEAM_LINE'])
    game_db = pd.concat([game_db, game_db_upload], ignore_index=True)
