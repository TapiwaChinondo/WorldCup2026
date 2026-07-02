# World Cup 2026 predictor 

This is a project created to see if AI can be used to accurately decide the winner of games and the 2026 tournament based on statistcis from the last 4 years as well as Fifa Ranking. 

## Functions 

- python src/predict_match.py "England" "DR Congo"
    - Predics the result of a singular match 
- python src/predict_fixtures.py fixtures/round_of_32.csv 
    - Predicts the results of a set of fixtures in a fixtures csv file
- python src/tournament_odds.py elo 10000
    - Simulates the tournament form the round of 32 to the final a specified number of times and prints out the % of times a team wins it


## notes

* High level Ai for score predicaiton is fairly basic and only predicts 1-0 / 2-0 / 3-0 or 1-1
and never a combiantion such as 2-1 or 2-2 though those are less common, 2-1 could be seen as a probable score line.