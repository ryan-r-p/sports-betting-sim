## Betting Sim v0.1

The Betting Sim is being designed to simulate a sports betting app and is a project that I'm working with to gain a
more familiarity with object-oriented programming and RESTful APIs.

In its current state, the program essentially functions as a large calculator (main.py) with functionality for placing
different types of sports bets (Straight Bet, Parlay, Round Robin) and persisting them in a multiple databases which
will allow us to track past bets and apply bet winnings to a player's bank after the related bet/future has settled.

I'm currently using dummy data to track application of the logic within the betting objects and logs, but I plan to
utilize the Odds API to pull in real-time game information and odds on a date-by-date basis.

To run the project in its current state, run either main.py to generate a 6-leg round-robin bet calculation using the
betting objects and the betting logs. You can also run investigation.py within the Odds_API folder to get a better
understanding of what I am trying to accomplish with the import of real-time sports and game information.
_________________________________________________

#### Constraints:

##### Always tandem upload information to DB and objects

-Bet Types: Straight Bet, Round Robin, Parlay

-Leg Types: To reflect the varying leg types reflected within the Odds API (TBD)

-Max Number of Legs: 10 (Parlay and Round Robin)

________________________________________________

TODO:

       1. Create a way to load attribute data into an object from the database
       2. Populate the leg objects with information from the Odds API after performing some sort of selection of upcoming
          games to bet, preferably from multiple leagues at once
                i. Could be accomplished through the use of a "current game" object, e.g. once a game is selected it can
                    be placed within an object for further use
                ii. UI or text-based UI needed to actually select the game from the list, preferably with a combination
                    of straight, points, and over/under combinations
       3. Create a way to enter a custom leg - the Odds API is not all-encompassing (especially for player stats),
          and I don't really care what people bet on.
                i. UI tool or text-based entry for creation of custom legs
                ii. Will require a manual entry for outcomes