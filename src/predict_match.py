import sys

from data.download import load_matches
from teams.manager import TeamManager
from models.poisson import PoissonPredictor


def main():
    if len(sys.argv) != 3:
        print("Usage: python src/predict_match.py 'Team A' 'Team B'")
        return

    team_a_name = sys.argv[1]
    team_b_name = sys.argv[2]

    matches = load_matches()
    manager = TeamManager(matches)

    predictor = PoissonPredictor(max_goals=6)

    team_a = manager[team_a_name]
    team_b = manager[team_b_name]

    prediction = predictor.predict(team_a, team_b)

    print(prediction)


if __name__ == "__main__":
    main()