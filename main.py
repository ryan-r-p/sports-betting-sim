import betting_objects as bob
import arrow  # better datetime functions
from tzlocal import get_localzone  # grabbing local timezone for conversions from UTC
import betting_logs as blog

# getting the time - local and utc || append everything in UTC always

current_time = arrow.utcnow()
bet_placed_tm = current_time
output_time_now = bet_placed_tm.to(str(get_localzone()))


# starting up the betting logs

bdb = blog.bet_db
ldb = blog.leg_db
rrdb = blog.round_robin_db

# creating betting objects - will update to append information from Odds API, for now we use dummy data from Wk 11

b1 = bob.Bet(1, 6, 3, 'Round Robin', '', 0, 14.00, 0, 0, True, '', False, current_time, '')
l1 = bob.Leg(1, 1, 'Carolina Panthers', '+500', 0, 'Game', 'NFL', 'Carolina Panthers @ Baltimore Ravens',
                   '11/20/2022', 'Pre-Game', '', '', True, False, bet_placed_tm, '')
l2 = bob.Leg(2, 1, 'Indianapolis Colts', '+235', 0, 'Game', 'NFL', 'Philadelphia Eagles @ Indianapolis Colts',
                   '11/20/2022', 'Pre-Game', '', '', True, False, bet_placed_tm, '')
l3 = bob.Leg(3, 1, 'New York Jets', '+154', 0, 'Game', 'NFL', 'New York Jets @ New England Patriots',
                   '11/20/2022', 'Pre-Game', '', '', True, False, bet_placed_tm, '')
l4 = bob.Leg(4, 1, 'Houston Texans', '+140', 0, 'Game', 'NFL', 'Washington Commanders @ Houston Texans',
                   '11/20/2022', 'Pre-Game', '', '', True, False, bet_placed_tm, '')
l5 = bob.Leg(5, 1, 'Los Angeles Rams', '+118', 0, 'Game', 'NFL', 'Los Angeles Rams @ New Orleans Saints',
                   '11/20/2022', 'Pre-Game', '', '', True, False, bet_placed_tm, '')
l6 = bob.Leg(6, 1, 'Detroit Lions', '+142', 0, 'Game', 'NFL', 'Detroit Lions @ New York Giants', '11/20/2022',
                   'Pre-Game', '', '', True, False, bet_placed_tm, '')

# applying bet objects to the logs

bdb = b1.dump_bet_to_log(bdb)
ldb = l1.dump_leg_to_log(ldb)
ldb = l2.dump_leg_to_log(ldb)
ldb = l3.dump_leg_to_log(ldb)
ldb = l4.dump_leg_to_log(ldb)
ldb = l5.dump_leg_to_log(ldb)
ldb = l6.dump_leg_to_log(ldb)

# applying the bet amount for red robin bet

b1.apply_bet_amount()

# applying decimal, american odds to bets

l1.apply_dec_odds()
ldb = blog.leg_dec_odds(ldb, l1.leg_id, l1.decimal_odds)

l2.apply_dec_odds()
ldb = blog.leg_dec_odds(ldb, l2.leg_id, l2.decimal_odds)

l3.apply_dec_odds()
ldb = blog.leg_dec_odds(ldb, l3.leg_id, l3.decimal_odds)

l4.apply_dec_odds()
ldb = blog.leg_dec_odds(ldb, l4.leg_id, l4.decimal_odds)

l5.apply_dec_odds()
ldb = blog.leg_dec_odds(ldb, l5.leg_id, l5.decimal_odds)

l6.apply_dec_odds()
ldb = blog.leg_dec_odds(ldb, l6.leg_id, l6.decimal_odds)

rr_list = blog.round_robin_list(ldb, b1.bet_id, b1.rr_num_picks)
rrdb = blog.round_robin_append(rr_list, ldb, rrdb, blog.set_round_robin_id(rrdb), b1.bet_id, b1.bet_amount)
rr_calc = blog.round_robin_calculate(rrdb, b1.bet_id)

bdb = blog.apply_round_robin_winnings(bdb, b1.bet_id, rr_calc[0], rr_calc[1])

b = blog.set_bet_id(bdb)

print(1)
