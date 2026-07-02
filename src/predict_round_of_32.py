from data.download import load_matches

from teams.manager import TeamManager
from ratings.elo import EloRatingManager

from models.ml_poisson import MLPoissonPredictor


ROUND_OF_32_FIXTURES = [
    ("South Africa", "Canada"),
    ("Brazil", "Japan"),
    ("Germany", "Paraguay"),
    ("Netherlands", "Morocco"),
    ("Ivory Coast", "Norway"),
    ("France", "Sweden"),
    ("Mexico", "Ecuador"),
    ("England", "DR Congo"),
    ("Belgium", "Senegal"),
    ("United States", "Bosnia and Herzegovina"),
    ("Spain", "Austria"),
    ("Portugal", "Croatia"),
    ("Switzerland", "Algeria"),
    ("Australia", "Egypt"),
    ("Argentina", "Cape Verde"),
    ("Colombia", "Ghana"),
]


def attach_elo_to_teams(manager, elo_manager):
    for team in manager.all_teams():
        team.elo = elo_manager.get_rating(team.name)


def main():
    matches = load_matches()

    manager = TeamManager(matches)

    elo_manager = EloRatingManager()
    elo_manager.process_matches(matches)

    attach_elo_to_teams(manager, elo_manager)

    predictor = MLPoissonPredictor(
        model_path="models/goal_model.pkl",
        max_goals=6
    )

    print("\nRound of 32 Score Predictions\n")

    for team_a_name, team_b_name in ROUND_OF_32_FIXTURES:
        team_a = manager[team_a_name]
        team_b = manager[team_b_name]

        prediction = predictor.predict(team_a, team_b)

        print(prediction)
        print("-" * 40)


if __name__ == "__main__":
    main()