import pandas as pd
import betting_objects as bob
import numpy as np
import itertools
import math

bet_db = pd.DataFrame(columns=['BET_ID', 'NUM_LEGS', 'RR_PICKS', 'BET_TYPE', 'ODDS', 'DECIMAL_ODDS',
                               'BET_AMOUNT', 'BET_WINNINGS', 'ACTUAL_WINNINGS', 'IN_PLAY', 'OUTCOME',
                               'BET_WON', 'TIME_BET_PLACED', 'TIME_BET_SETTLED'])

leg_db = pd.DataFrame(columns=['LEG_ID', 'BET_ID', 'LEG_NAME', 'ODDS', 'DECIMAL_ODDS',  'LEG_TYPE',
                               'LEAGUE', 'GAME', 'GAME_TIME', 'GAME_PROGRESS', 'GAME_OUTCOME', 'LEG_OUTCOME',
                               'IN_PLAY', 'LEG_WON', 'LEG_PLACED_TM', 'LEG_SETTLED_TM'])

round_robin_db = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'COMBINED_ODDS', 'COMBINED_OUTCOME',
                                       'SPLIT_BET_AMOUNT', 'SPLIT_WINNINGS', 'LEG_ID_1', 'LEG_1_ODDS', 'LEG_1_OUTCOME',
                                       'LEG_ID_2', 'LEG_2_ODDS', 'LEG_2_OUTCOME', 'LEG_ID_3', 'LEG_3_ODDS',
                                       'LEG_3_OUTCOME', 'LEG_ID_4', 'LEG_4_ODDS', 'LEG_4_OUTCOME', 'LEG_ID_5',
                                       'LEG_5_ODDS', 'LEG_5_OUTCOME', 'LEG_ID_6', 'LEG_6_ODDS', 'LEG_6_OUTCOME',
                                       'LEG_ID_7', 'LEG_7_ODDS', 'LEG_7_OUTCOME', 'LEG_ID_8', 'LEG_8_ODDS',
                                       'LEG_8_OUTCOME', 'LEG_ID_9', 'LEG_9_ODDS', 'LEG_9_OUTCOME', 'LEG_ID_10',
                                       'LEG_10_ODDS', 'LEG_10_OUTCOME'])


def clear_log(df):  # clear df and leave columns
    df = df[0:0]
    return df


def set_bet_id(bet_df):  # set bet_id within the bet df based off of previous bet_id
    if bet_df.empty:
        bet_id = 1
    else:
        a = bet_df
        a = a['BET_ID'].iloc[-1]
        bet_id = int(a + 1)
    return bet_id


def set_leg_id(leg_df):  # set bet_id within the leg df based off of the previous leg_id
    if leg_df.empty:
        leg_id = 1
    else:
        a = leg_df
        a = a['LEG_ID'].iloc[-1]
        leg_id = int(a + 1)
    return leg_id


def set_round_robin_id(round_robin_df):  # set round-robin id within the round-robin df based off previous rr id
    if round_robin_df.empty:
        rr_id = 1
    else:
        a = round_robin_df
        a = a['ROUND_ROBIN_ID'].iloc[-1]
        rr_id = int(a + 1)
    return rr_id


def set_bet_amount(bet_df, bet_id, bet_amount):  # applies bet amount to bet_db based on bob.Bet.apply_bet_amount
    if bet_df['BET_ID'] == bet_id:
        bet_df['BET_AMOUNT'] = bet_amount


def count_legs(leg_df, bet_id):  # count number of legs in leg_db for specific bet_id
    a = str(bet_id)
    b = leg_df.query(('BET_ID == '+str(a)))
    c = len(b.index)
    return c


def bet_dec_odds(bet_df, bet_id, dec_odds):  # applies decimal odds to bet logs - use with bob.dec_odds()
    a = bet_df
    a = a.set_index('BET_ID')
    a.at[bet_id, 'DECIMAL_ODDS'] = dec_odds
    a = a.reset_index()
    return a


def leg_dec_odds(leg_df, leg_id, dec_odds):  # applies decimal odds to leg logs - use with bob.dec_odds()
    a = leg_df
    a = a.set_index('LEG_ID')
    a.at[leg_id, 'DECIMAL_ODDS'] = dec_odds
    a = a.reset_index()
    return a


def apply_parlay_odds(leg_df, bet_id):  # create list of odds for all legs, find sum for all straight bets and parlays
    a = str(bet_id)
    b = leg_df
    b = b.query(("BET_ID == "+a))
    b = b['DECIMAL_ODDS'].to_list()
    c = np.prod(b)
    return c


def apply_parlay_winnings(bet_df, bet_id, dec_odds, bet_amount):
    # applies calculated odds/winnings to bet_id from obj for straight bets and parlays
    a = bet_df
    b = int(bet_id)
    a = a.set_index('BET_ID')
    a.at[b, 'ODDS'] = bob.dec_to_amer(dec_odds)
    a.at[b, 'DECIMAL_ODDS'] = dec_odds
    a.at[b, 'BET_WINNINGS'] = round(bet_amount * dec_odds, 2)
    a = a.reset_index()
    return a


def apply_round_robin_winnings(bet_df, bet_id, winnings, dec_odds):
    # applies calculated odds/winnings to bet_id from rr_db for round-robin bets
    a = bet_df
    b = int(bet_id)
    a = a.set_index('BET_ID')
    a.at[b, 'ODDS'] = bob.dec_to_amer(dec_odds)
    a.at[b, 'DECIMAL_ODDS'] = dec_odds
    a.at[b, 'BET_WINNINGS'] = winnings
    a = a.reset_index()
    return a


def round_robin_list(leg_df, bet_id, picks):  # generate list of round-robin combos based on len of legs in bet_id
    a = str(bet_id)
    df = leg_df
    df = df.query("BET_ID == "+a)
    b = df["LEG_ID"].to_list()
    if picks == 2:
        rr_list = list(itertools.combinations(b, 2))
    elif picks == 3:
        rr_list = list(itertools.combinations(b, 3))
    elif picks == 4:
        rr_list = list(itertools.combinations(b, 4))
    elif picks == 5:
        rr_list = list(itertools.combinations(b, 5))
    elif picks == 6:
        rr_list = list(itertools.combinations(b, 6))
    elif picks == 7:
        rr_list = list(itertools.combinations(b, 7))
    elif picks == 8:
        rr_list = list(itertools.combinations(b, 8))
    elif picks == 9:
        rr_list = list(itertools.combinations(b, 9))
    else:
        rr_list = []
    return rr_list


def round_robin_append(rr_list, leg_df, rr_df, rr_id, bet_id, bet_amount):
    # Append new round-robin bets to the round-robin db
    num_picks = len(rr_list[0])
    bet_id = int(bet_id)
    bet_amount = float(bet_amount)
    x = rr_df
    y = leg_df
    y = y.set_index('LEG_ID')

    if num_picks == 2:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    elif num_picks == 3:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS',  'LEG_ID_3', 'LEG_3_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            id3 = int(i[2])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            odds3 = y.at[id3, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2, id3,
                                 odds3]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    elif num_picks == 4:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS',  'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4', 'LEG_4_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            id3 = int(i[2])
            id4 = int(i[3])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            odds3 = y.at[id3, 'DECIMAL_ODDS']
            odds4 = y.at[id4, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2, id3,
                                 odds3, id4, odds4]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4',
                                        'LEG_4_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    elif num_picks == 5:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS',  'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4', 'LEG_4_ODDS',
                                   'LEG_ID_5', 'LEG_5_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            id3 = int(i[2])
            id4 = int(i[3])
            id5 = int(i[4])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            odds3 = y.at[id3, 'DECIMAL_ODDS']
            odds4 = y.at[id4, 'DECIMAL_ODDS']
            odds5 = y.at[id5, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2, id3,
                                 odds3, id4, odds4, id5, odds5]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4',
                                        'LEG_4_ODDS', 'LEG_ID_5', 'LEG_5_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    elif num_picks == 6:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS',  'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4', 'LEG_4_ODDS',
                                   'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            id3 = int(i[2])
            id4 = int(i[3])
            id5 = int(i[4])
            id6 = int(i[5])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            odds3 = y.at[id3, 'DECIMAL_ODDS']
            odds4 = y.at[id4, 'DECIMAL_ODDS']
            odds5 = y.at[id5, 'DECIMAL_ODDS']
            odds6 = y.at[id6, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2, id3,
                                 odds3, id4, odds4, id5, odds5, id6, odds6]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4',
                                        'LEG_4_ODDS', 'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    elif num_picks == 7:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS',  'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4', 'LEG_4_ODDS',
                                   'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS',
                                   'LEG_ID_7', 'LEG_7_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            id3 = int(i[2])
            id4 = int(i[3])
            id5 = int(i[4])
            id6 = int(i[5])
            id7 = int(i[6])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            odds3 = y.at[id3, 'DECIMAL_ODDS']
            odds4 = y.at[id4, 'DECIMAL_ODDS']
            odds5 = y.at[id5, 'DECIMAL_ODDS']
            odds6 = y.at[id6, 'DECIMAL_ODDS']
            odds7 = y.at[id7, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2, id3,
                                 odds3, id4, odds4, id5, odds5, id6, odds6, id7, odds7]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4',
                                        'LEG_4_ODDS', 'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS', 'LEG_ID_7',
                                        'LEG_7_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    elif num_picks == 8:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4', 'LEG_4_ODDS',
                                   'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS',
                                   'LEG_ID_7', 'LEG_7_ODDS', 'LEG_ID_8', 'LEG_8_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            id3 = int(i[2])
            id4 = int(i[3])
            id5 = int(i[4])
            id6 = int(i[5])
            id7 = int(i[6])
            id8 = int(i[7])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            odds3 = y.at[id3, 'DECIMAL_ODDS']
            odds4 = y.at[id4, 'DECIMAL_ODDS']
            odds5 = y.at[id5, 'DECIMAL_ODDS']
            odds6 = y.at[id6, 'DECIMAL_ODDS']
            odds7 = y.at[id7, 'DECIMAL_ODDS']
            odds8 = y.at[id8, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2, id3,
                                 odds3, id4, odds4, id5, odds5, id6, odds6, id7, odds7, id8, odds8]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4',
                                        'LEG_4_ODDS', 'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS', 'LEG_ID_7',
                                        'LEG_7_ODDS', 'LEG_ID_8', 'LEG_8_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    elif num_picks == 9:
        df = pd.DataFrame(columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1', 'LEG_1_ODDS',
                                   'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4', 'LEG_4_ODDS',
                                   'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS',
                                   'LEG_ID_7', 'LEG_7_ODDS', 'LEG_ID_8', 'LEG_8_ODDS', 'LEG_ID_9', 'LEG_9_ODDS'])
        for i in rr_list:
            rr_id = int(rr_id)
            id1 = int(i[0])
            id2 = int(i[1])
            id3 = int(i[2])
            id4 = int(i[3])
            id5 = int(i[4])
            id6 = int(i[5])
            id7 = int(i[6])
            id8 = int(i[7])
            id9 = int(i[8])
            odds1 = y.at[id1, 'DECIMAL_ODDS']
            odds2 = y.at[id2, 'DECIMAL_ODDS']
            odds3 = y.at[id3, 'DECIMAL_ODDS']
            odds4 = y.at[id4, 'DECIMAL_ODDS']
            odds5 = y.at[id5, 'DECIMAL_ODDS']
            odds6 = y.at[id6, 'DECIMAL_ODDS']
            odds7 = y.at[id7, 'DECIMAL_ODDS']
            odds8 = y.at[id8, 'DECIMAL_ODDS']
            odds9 = y.at[id9, 'DECIMAL_ODDS']
            df1 = pd.DataFrame([[rr_id, bet_id, num_picks, (bet_amount / len(rr_list)), id1, odds1, id2, odds2, id3,
                                 odds3, id4, odds4, id5, odds5, id6, odds6, id7, odds7, id8, odds8, id9, odds9]],
                               columns=['ROUND_ROBIN_ID', 'BET_ID', 'PICKS', 'SPLIT_BET_AMOUNT', 'LEG_ID_1',
                                        'LEG_1_ODDS', 'LEG_ID_2', 'LEG_2_ODDS', 'LEG_ID_3', 'LEG_3_ODDS', 'LEG_ID_4',
                                        'LEG_4_ODDS', 'LEG_ID_5', 'LEG_5_ODDS', 'LEG_ID_6', 'LEG_6_ODDS', 'LEG_ID_7',
                                        'LEG_7_ODDS', 'LEG_ID_8', 'LEG_8_ODDS', 'LEG_ID_9', 'LEG_9_ODDS'])
            df = pd.concat([df, df1], ignore_index=True)
            rr_id += 1
    else:
        print("Number of legs is out of range...")
        return 'NaN'

    x = pd.concat([x, df], ignore_index=True)
    return x


def round_robin_calculate(rr_df, bet_id):
    # perform calculation to get max win amt and mean of decimal odds to append within the round-robin db
    combined_odds = float(0)
    for i in rr_df.index:
        if rr_df['BET_ID'][i] == bet_id:
            if math.isnan(rr_df['LEG_1_ODDS'][i]) is True:
                odds1 = 1
            else:
                odds1 = rr_df['LEG_1_ODDS'][i]
            if math.isnan(rr_df['LEG_2_ODDS'][i]) is True:
                odds2 = 1
            else:
                odds2 = rr_df['LEG_2_ODDS'][i]
            if math.isnan(rr_df['LEG_3_ODDS'][i]) is True:
                odds3 = 1
            else:
                odds3 = rr_df['LEG_3_ODDS'][i]
            if math.isnan(rr_df['LEG_4_ODDS'][i]) is True:
                odds4 = 1
            else:
                odds4 = rr_df['LEG_4_ODDS'][i]
            if math.isnan(rr_df['LEG_5_ODDS'][i]) is True:
                odds5 = 1
            else:
                odds5 = rr_df['LEG_5_ODDS'][i]
            if math.isnan(rr_df['LEG_6_ODDS'][i]) is True:
                odds6 = 1
            else:
                odds6 = rr_df['LEG_6_ODDS'][i]
            if math.isnan(rr_df['LEG_7_ODDS'][i]) is True:
                odds7 = 1
            else:
                odds7 = rr_df['LEG_7_ODDS'][i]
            if math.isnan(rr_df['LEG_8_ODDS'][i]) is True:
                odds8 = 1
            else:
                odds8 = rr_df['LEG_8_ODDS'][i]
            if math.isnan(rr_df['LEG_9_ODDS'][i]) is True:
                odds9 = 1
            else:
                odds9 = rr_df['LEG_9_ODDS'][i]

            combined_odds = odds1 * odds2 * odds3 * odds4 * odds5 * odds6 * odds7 * odds8 * odds9

        rr_df.at[i, 'COMBINED_ODDS'] = combined_odds

        split_bet_amt = rr_df.at[i, 'SPLIT_BET_AMOUNT']
        winnings = combined_odds * split_bet_amt
        rr_df.at[i, 'SPLIT_WINNINGS'] = float(round(winnings, 2))

    return rr_df['SPLIT_WINNINGS'].sum(), round(rr_df['COMBINED_ODDS'].mean(), 2)
