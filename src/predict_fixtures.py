import sys
from pathlib import Path

import pandas as pd

from data.download import load_matches
from teams.manager import TeamManager
from ratings.elo import EloRatingManager
from models.ml_poisson import MLPoissonPredictor


def attach_elo_to_teams(manager, elo_manager):
    for team in manager.all_teams():
        team.elo = elo_manager.get_rating(team.name)


def load_fixtures(path):
    fixtures = pd.read_csv(path)

    required_columns = {"team_a", "team_b"}

    if not required_columns.issubset(fixtures.columns):
        raise ValueError(
            "Fixture CSV must contain columns: team_a, team_b"
        )

    return fixtures


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/predict_fixtures.py fixtures/round_of_32.csv")
        return

    fixture_file = Path(sys.argv[1])

    matches = load_matches()

    manager = TeamManager(matches)

    elo_manager = EloRatingManager()
    elo_manager.process_matches(matches)

    attach_elo_to_teams(manager, elo_manager)

    predictor = MLPoissonPredictor(
        model_path="models/goal_model_v2.pkl",
        max_goals=6
    )

    fixtures = load_fixtures(fixture_file)

    print(f"\nPredictions for {fixture_file}\n")

    for _, fixture in fixtures.iterrows():
        team_a = manager[fixture["team_a"]]
        team_b = manager[fixture["team_b"]]

        prediction = predictor.predict(team_a, team_b)

        print(prediction)
        print("-" * 40)


if __name__ == "__main__":
    main()