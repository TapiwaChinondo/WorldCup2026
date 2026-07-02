from pathlib import Path
import sys
from collections import defaultdict, deque

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

import joblib
import pandas as pd

from data.download import load_matches
from ratings.elo import EloRatingManager
from matches.match import Match


MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "goal_model_v2.pkl"


TOURNAMENT_WEIGHTS = {
    "FIFA World Cup": 5,
    "FIFA World Cup qualification": 3,
    "UEFA Euro": 4,
    "Copa América": 4,
    "African Cup of Nations": 4,
    "AFC Asian Cup": 4,
    "CONCACAF Gold Cup": 4,
    "UEFA Nations League": 2,
    "Friendly": 1,
}


def tournament_weight(name):
    return TOURNAMENT_WEIGHTS.get(name, 2)


def empty_stats():
    return {
        "matches": 0,
        "goals_for": 0,
        "goals_against": 0,
        "wins": 0,
        "recent": deque(maxlen=10),
    }


def goals_per_game(stats):
    if stats["matches"] == 0:
        return 1.0
    return stats["goals_for"] / stats["matches"]


def goals_against_per_game(stats):
    if stats["matches"] == 0:
        return 1.0
    return stats["goals_against"] / stats["matches"]


def win_percentage(stats):
    if stats["matches"] == 0:
        return 0.33
    return stats["wins"] / stats["matches"]


def recent_goals_for(stats):
    recent = stats["recent"]
    if not recent:
        return goals_per_game(stats)
    return sum(match["goals_for"] for match in recent) / len(recent)


def recent_goals_against(stats):
    recent = stats["recent"]
    if not recent:
        return goals_against_per_game(stats)
    return sum(match["goals_against"] for match in recent) / len(recent)


def recent_win_percentage(stats):
    recent = stats["recent"]
    if not recent:
        return win_percentage(stats)
    return sum(match["win"] for match in recent) / len(recent)


def add_team_row(team, opponent, team_goals, team_elo, opponent_elo, is_home, is_neutral, tournament, team_stats, opponent_stats):
    return {
        "team_elo": team_elo,
        "opponent_elo": opponent_elo,
        "elo_difference": team_elo - opponent_elo,

        "is_home": is_home,
        "is_neutral": is_neutral,
        "tournament_weight": tournament_weight(tournament),

        "team_goals_per_game": goals_per_game(team_stats),
        "opponent_goals_against_per_game": goals_against_per_game(opponent_stats),

        "team_recent_goals_per_game": recent_goals_for(team_stats),
        "opponent_recent_goals_against_per_game": recent_goals_against(opponent_stats),

        "team_win_percentage": win_percentage(team_stats),
        "team_recent_win_percentage": recent_win_percentage(team_stats),

        "goals": team_goals,
    }


def update_stats(stats, goals_for, goals_against):
    stats["matches"] += 1
    stats["goals_for"] += goals_for
    stats["goals_against"] += goals_against

    win = 1 if goals_for > goals_against else 0
    stats["wins"] += win

    stats["recent"].append({
        "goals_for": goals_for,
        "goals_against": goals_against,
        "win": win,
    })


def build_training_data(matches):
    matches = matches.copy()
    matches["date"] = pd.to_datetime(matches["date"])
    matches = matches.sort_values("date")

    elo = EloRatingManager()
    team_stats = defaultdict(empty_stats)

    rows = []

    for _, row in matches.iterrows():
        if row[["home_score", "away_score"]].isna().any():
            continue

        home = row["home_team"]
        away = row["away_team"]

        home_goals = row["home_score"]
        away_goals = row["away_score"]

        home_elo = elo.get_rating(home)
        away_elo = elo.get_rating(away)

        rows.append(add_team_row(
            home, away, home_goals,
            home_elo, away_elo,
            is_home=1,
            is_neutral=int(row["neutral"]),
            tournament=row["tournament"],
            team_stats=team_stats[home],
            opponent_stats=team_stats[away],
        ))

        rows.append(add_team_row(
            away, home, away_goals,
            away_elo, home_elo,
            is_home=0,
            is_neutral=int(row["neutral"]),
            tournament=row["tournament"],
            team_stats=team_stats[away],
            opponent_stats=team_stats[home],
        ))

        match = Match(
            date=row["date"],
            home_team=home,
            away_team=away,
            home_score=home_goals,
            away_score=away_goals,
            tournament=row["tournament"],
            city=row["city"],
            country=row["country"],
            neutral=row["neutral"],
        )

        elo.update_match(match)

        update_stats(team_stats[home], home_goals, away_goals)
        update_stats(team_stats[away], away_goals, home_goals)

    return pd.DataFrame(rows)


def main():
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error

    matches = load_matches()
    data = build_training_data(matches)

    features = [
        "team_elo",
        "opponent_elo",
        "elo_difference",
        "is_home",
        "is_neutral",
        "tournament_weight",
        "team_goals_per_game",
        "opponent_goals_against_per_game",
        "team_recent_goals_per_game",
        "opponent_recent_goals_against_per_game",
        "team_win_percentage",
        "team_recent_win_percentage",
    ]

    X = data[features]
    y = data["goals"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        min_samples_leaf=8,
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    print(f"Training rows: {len(data)}")
    print(f"Mean Absolute Error: {mae:.3f} goals")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    print(f"Saved model to {MODEL_FILE}")


if __name__ == "__main__":
    main()