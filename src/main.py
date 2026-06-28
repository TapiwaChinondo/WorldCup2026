from data.download import load_matches


def main():
    matches = load_matches()
    print(matches.head())


if __name__ == "__main__":
    main()