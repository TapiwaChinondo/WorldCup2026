from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(SRC_DIR))

import joblib
import pandas as pd

from data.download import load_matches
from ratings.elo import EloRatingManager


MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "goal_model.pkl"


def build_training_data(matches):
    matches = matches.copy()
    matches["date"] = pd.to_datetime(matches["date"])
    matches = matches.sort_values("date")

    elo = EloRatingManager()

    rows = []

    for _, row in matches.iterrows():
        if row[["home_score", "away_score"]].isna().any():
            continue

        home = row["home_team"]
        away = row["away_team"]

        home_elo = elo.get_rating(home)
        away_elo = elo.get_rating(away)

        rows.append({
            "team_elo": home_elo,
            "opponent_elo": away_elo,
            "elo_difference": home_elo - away_elo,
            "is_home": 1,
            "is_neutral": int(row["neutral"]),
            "goals": row["home_score"],
        })

        rows.append({
            "team_elo": away_elo,
            "opponent_elo": home_elo,
            "elo_difference": away_elo - home_elo,
            "is_home": 0,
            "is_neutral": int(row["neutral"]),
            "goals": row["away_score"],
        })

        from matches.match import Match

        match = Match(
            date=row["date"],
            home_team=home,
            away_team=away,
            home_score=row["home_score"],
            away_score=row["away_score"],
            tournament=row["tournament"],
            city=row["city"],
            country=row["country"],
            neutral=row["neutral"],
        )

        elo.update_match(match)

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
        n_estimators=200,
        random_state=42,
        min_samples_leaf=10,
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