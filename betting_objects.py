import betting_logs as blog
import itertools
import pandas as pd


def amer_to_dec(american_odds):  # convert from American odds to decimal odds
    o = int(american_odds)
    if o >= 0:
        a = (o / 100) + 1
    else:
        a = (100 / abs(o)) + 1
    return float(a)


def dec_to_amer(decimal_odds):  # convert from decimal odds to American odds
    o = float(decimal_odds)
    if o >= 2.0:
        a = int(round((o - 1) * 100, 0))
    else:
        a = int(round((-100) / (decimal_odds - 1), 0))
    if a >= 0:
        a = "+" + str(a)
    else:
        a = str(a)
    return a


class PlayerBank:
    def __init__(self, bank_amt, in_play):
        self.bank_amt = float(bank_amt)  # player total bank
        self.in_play = float(in_play)  # amount currently in play

    def buy_in(self, buy_in):  # "buy in" to the game
        if self.bank_amt == 0:
            self.bank_amt = float(buy_in)
        else:
            self.bank_amt = float(buy_in) + self.bank_amt

    def cash_out(self, cash_out_amt):  # "cash out" from the game
        self.bank_amt = self.bank_amt - float(cash_out_amt)

    def adjust_balance(self, plyr_input):  # adjust player bank balance, does not affect in play
        self.bank_amt = float(plyr_input)

    def place_bet(self, bet_amount):  # adjust balance after bet placed
        if self.bank_amt >= float(bet_amount):
            self.bank_amt = self.bank_amt - float(bet_amount)
            self.in_play = self.in_play + float(bet_amount)

    def settle_bet(self, bet_won, winnings, bet_amount):  # settle the bet after game conclusion
        if bet_won is True:
            self.bank_amt = self.bank_amt + float(winnings)
            self.in_play = self.in_play - float(bet_amount)
        else:
            self.in_play = self.in_play - float(bet_amount)


class Bet:
    def __init__(self, bet_id, num_legs, rr_num_picks, bet_type, odds, decimal_odds, bet_amount, total_winnings,
                 actual_winnings, in_play, bet_outcome, bet_won, bet_placed_tm, bet_settled_tm):
        self.bet_id = int(bet_id)  # a unique id for each bet
        self.num_legs = int(num_legs)  # number of legs within bet
        self.rr_num_picks = int(rr_num_picks)
        self.bet_type = bet_type  # type of bet (Straight Bet, Parlay, or Round Robin)
        self.odds = odds  # American-formatted odds
        self.decimal_odds = decimal_odds  # conversion of american odds to decimal odds
        self.bet_amount = float(bet_amount)  # Amount of bet placed
        self.total_winnings = float(total_winnings)  # Amount of total potential winnings
        self.actual_winnings = float(actual_winnings)
        self.in_play = bool(in_play)  # True/false indicating if bet is in play
        self.bet_outcome = bet_outcome  # Tracking the outcome of the bet
        self.bet_won = bool(bet_won)  # True/false indicating if bet won
        self.bet_placed_tm = bet_placed_tm  # Time bet placed
        self.bet_settled_tm = bet_settled_tm  # Time bet settled

    def apply_bet_amount(self):  # apply bet amount based on bet type - straight bets/parlays and red-robin bets
        if self.bet_type == 'Straight Bet' or 'Parlay':
            self.bet_amount = self.bet_amount
        if self.bet_type == 'Round Robin':
            self.bet_amount = (self.bet_amount * len(list(itertools.combinations(range(0, self.num_legs),
                                                                                 self.rr_num_picks))))

    def apply_dec_odds(self):  # convert from American odds to decimal odds
        o = amer_to_dec(int(self.odds))
        self.decimal_odds = o
        return o

    def apply_winnings(self):  # get total potential winnings based on decimal odds of bet
        self.total_winnings = round((self.decimal_odds * self.bet_amount), 2)

    def to_win_amt(self):  # get "to-win" amount for bet (minus any placed bets)
        a = self.total_winnings - self.bet_amount
        return a

    def count_num_legs(self, leg_db):  # count number of legs contained in a bet id
        a = blog.count_legs(leg_db, self.bet_id)
        self.num_legs = int(a)

    def apply_parlay_odds(self, leg_db):  # grabbing output from blog.parlay_odds, giving output to odds
        a = blog.apply_parlay_odds(leg_db, self.bet_id)
        self.decimal_odds = a
        b = dec_to_amer(a)
        self.odds = str(b)

    def apply_round_robin_calc(self, bet_id, bet_db):
        if self.bet_type == 'Round Robin':
            self.total_winnings = bet_db.at[bet_id, 'BET_WINNINGS']
            self.decimal_odds = bet_db.at[bet_id, 'DECIMAL_ODDS']
            self.odds = bet_db.at[bet_id, 'ODDS']

    # Bet attribute update functions:

    def update_bet_id(self, new_bet_id):  # apply new bet id when placing bet - applies from betting_logs.set_bet_id
        self.bet_id = new_bet_id

    def update_num_legs(self, new_num_legs):
        self.num_legs = int(new_num_legs)

    def update_bet_type(self, new_bet_type):
        if new_bet_type == 'Straight Bet' or new_bet_type == 'Parlay' or new_bet_type == 'Round Robin':
            self.bet_type = new_bet_type
        else:
            self.bet_type = self.bet_type

    def update_odds(self, new_odds):
        self.odds = new_odds

    def update_bet_amount(self, new_bet_amt):
        self.bet_amount = float(new_bet_amt)

    def update_in_play(self, new_in_play):
        if new_in_play is bool:
            self.in_play = bool(new_in_play)
        else:
            self.in_play = self.in_play

    def update_bet_outcome(self, new_bet_outcome):
        if new_bet_outcome == 'Won' or new_bet_outcome == 'Lost' or new_bet_outcome == '':
            self.bet_outcome = new_bet_outcome
        else:
            self.bet_outcome = self.bet_outcome

    def update_bet_won(self, new_bet_won):
        if new_bet_won is bool:
            self.bet_won = bool(new_bet_won)
        else:
            self.bet_won = self.bet_won

    def update_bet_placed_tm(self, new_bet_placed_tm):
        self.bet_placed_tm = new_bet_placed_tm

    def update_bet_settled_tm(self, new_bet_settled_tm):
        self.bet_settled_tm = new_bet_settled_tm

    # (simple) Attribute dump to db

    def dump_bet_to_log(self, bet_db):
        data = pd.DataFrame([[self.bet_id, self.num_legs, self.rr_num_picks, self.bet_type, self.odds,
                              self.decimal_odds, self.bet_amount, self.total_winnings, self.actual_winnings,
                              self.in_play, self.bet_outcome, self.bet_won, self.bet_placed_tm, self.bet_settled_tm]],
                            columns=['BET_ID', 'NUM_LEGS', 'RR_PICKS', 'BET_TYPE', 'ODDS', 'DECIMAL_ODDS', 'BET_AMOUNT',
                                     'BET_WINNINGS', 'ACTUAL_WINNINGS', 'IN_PLAY', 'OUTCOME', 'BET_WON',
                                     'TIME_BET_PLACED', 'TIME_BET_SETTLED']
                            )
        a = bet_db
        b = pd.concat([a, data])
        return b


class Leg:
    def __init__(self, leg_id, bet_id, leg_name, odds, decimal_odds, leg_type, league, game, game_time,
                 game_progress, game_outcome, leg_outcome, in_play, leg_won, leg_placed_tm, leg_settled_tm):
        self.leg_id = int(leg_id)  # unique id for each leg
        self.bet_id = int(bet_id)  # foreign key to bet db
        self.leg_name = leg_name  # name of bet / leg of bet
        self.odds = odds  # leg odds
        self.decimal_odds = float(decimal_odds)  # conversion of american odds to decimal odds to assign this attr
        self.leg_type = leg_type  # Game, Player Future, or Team Future
        self.league = league  # related sports league
        self.game = game  # related league game
        self.game_time = game_time  # time of start - related league game
        self.game_progress = game_progress  # progress of leg-related game at time of bet (Pre-game or game score)
        self.game_outcome = game_outcome  # outcome of leg-related game
        self.leg_outcome = leg_outcome  # outcome of leg
        self.in_play = bool(in_play)  # True/false indicating if leg is in play
        self.leg_won = bool(leg_won)  # True/false indicating if leg won
        self.leg_placed_tm = leg_placed_tm   # Time leg placed
        self.leg_settled_tm = leg_settled_tm  # Time bet settled

    def apply_dec_odds(self):  # convert from American odds to decimal odds
        o = amer_to_dec(int(self.odds))
        self.decimal_odds = o

    # Leg attribute update functions

    def update_leg_id(self, new_leg_id):  # apply new leg id when placing bet - applies from betting_logs.set_leg_id
        self.leg_id = int(new_leg_id)

    def update_bet_id(self, new_bet_id):
        self.bet_id = int(new_bet_id)

    def update_leg_name(self, new_leg_name):
        self.leg_name = new_leg_name

    def update_odds(self, new_odds):
        self.odds = new_odds

    def update_leg_type(self, new_leg_type):
        self.leg_type = new_leg_type

    def update_league(self, new_league):
        self.league = new_league

    def update_game(self, new_game):
        self.game = new_game

    def update_game_time(self, new_game_time):
        self.game_time = new_game_time

    def update_game_progress(self, new_game_progress):
        self.game_progress = new_game_progress

    def update_game_outcome(self, new_game_outcome):
        self.game_outcome = new_game_outcome

    def update_leg_outcome(self, new_leg_outcome):
        self.leg_outcome = new_leg_outcome

    def update_in_play(self, new_in_play):
        self.in_play = new_in_play

    def update_leg_won(self, new_leg_won):
        self.leg_won = new_leg_won

    def update_leg_placed_tm(self, new_leg_placed_tm):
        self.leg_placed_tm = new_leg_placed_tm

    def update_leg_settled_tm(self, new_game_time):
        self.game_time = new_game_time

    # Attribute dump to db
    def dump_leg_to_log(self, leg_db):
        data = pd.DataFrame([[self.leg_id, self.bet_id, self.leg_name, self.odds, self.decimal_odds, self.leg_type,
                              self.league, self.game, self.game_time, self.game_progress, self.game_outcome,
                              self.leg_outcome, self.in_play, self.leg_won, self.leg_placed_tm, self.leg_settled_tm]],
                            columns=['LEG_ID', 'BET_ID', 'LEG_NAME', 'ODDS', 'DECIMAL_ODDS', 'LEG_TYPE',
                                     'LEAGUE', 'GAME', 'GAME_TIME', 'GAME_PROGRESS', 'GAME_OUTCOME', 'LEG_OUTCOME',
                                     'IN_PLAY', 'LEG_WON', 'LEG_PLACED_TM', 'LEG_SETTLED_TM']
                            )
        a = leg_db
        b = pd.concat([a, data])
        return b
