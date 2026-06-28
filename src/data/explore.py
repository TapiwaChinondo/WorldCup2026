from download import load_matches


def main():
    matches = load_matches()

    print("\nDataset Shape")
    print(matches.shape)

    print("\nColumns")
    print(matches.columns.tolist())

    print("\nDate Range")
    print(matches["date"].min(), "->", matches["date"].max())

    print("\nNumber of tournaments")
    print(matches["tournament"].nunique())

    print("\nTop 15 tournaments")
    print(matches["tournament"].value_counts().head(15))

    teams = set(matches["home_team"]) | set(matches["away_team"])

    print("\nUnique teams")
    print(len(teams))

    print("\nMost matches played")

    appearances = (
        matches["home_team"]
        .value_counts()
        .add(matches["away_team"].value_counts(), fill_value=0)
        .sort_values(ascending=False)
    )

    print(appearances.head(20))


if __name__ == "__main__":
    main()