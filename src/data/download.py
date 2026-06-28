from pathlib import Path

import pandas as pd
import requests


URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"

DATA_DIR = Path("data/raw")
MATCHES_FILE = DATA_DIR / "results.csv"


def download_results():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading international football results...")

    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    MATCHES_FILE.write_bytes(response.content)

    print(f"Saved to {MATCHES_FILE}")


def load_matches():
    if not MATCHES_FILE.exists():
        raise FileNotFoundError(
            f"{MATCHES_FILE} does not exist. Run download_results() first."
        )

    df = pd.read_csv(MATCHES_FILE)

    print(f"Loaded {len(df)} matches.")

    return df


if __name__ == "__main__":
    download_results()