from pathlib import Path

from download import load_matches


OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "results_training.csv"


def preprocess():
    matches = load_matches()

    matches["date"] = matches["date"].astype("datetime64[ns]")

    matches = matches.sort_values("date")

    # Keep only the last World Cup cycle
    matches = matches[matches["date"] >= "2022-01-01"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    matches.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {len(matches)} matches.")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    preprocess()