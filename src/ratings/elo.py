#Elo system 

class EloRatingManager:

    def __init__(self, initial_rating=1500, k_factor=32):
        self.initial_rating = initial_rating
        self.k_factor = k_factor
        self.ratings = {}

    def get_rating(self, team_name):
        if team_name not in self.ratings:
            self.ratings[team_name] = self.initial_rating

        return self.ratings[team_name]

    def expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def actual_score(self, goals_for, goals_against):
        if goals_for > goals_against:
            return 1
        if goals_for < goals_against:
            return 0
        return 0.5

    def update_match(self, match):
        home_rating = self.get_rating(match.home_team)
        away_rating = self.get_rating(match.away_team)

        home_expected = self.expected_score(home_rating, away_rating)
        away_expected = self.expected_score(away_rating, home_rating)

        home_actual = self.actual_score(
            match.home_score,
            match.away_score
        )

        away_actual = 1 - home_actual

        self.ratings[match.home_team] = home_rating + self.k_factor * (
            home_actual - home_expected
        )

        self.ratings[match.away_team] = away_rating + self.k_factor * (
            away_actual - away_expected
        )

    def process_matches(self, matches):
        for _, row in matches.iterrows():

            if row[["home_score", "away_score"]].isna().any():
                continue

            from matches.match import Match

            match = Match(
                date=row["date"],
                home_team=row["home_team"],
                away_team=row["away_team"],
                home_score=row["home_score"],
                away_score=row["away_score"],
                tournament=row["tournament"],
                city=row["city"],
                country=row["country"],
                neutral=row["neutral"],
            )

            self.update_match(match)

    def top_ratings(self, n=20):
        return sorted(
            self.ratings.items(),
            key=lambda item: item[1],
            reverse=True
        )[:n]