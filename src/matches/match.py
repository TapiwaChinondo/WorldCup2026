class Match:

    def __init__(
        self,
        date,
        home_team,
        away_team,
        home_score,
        away_score,
        tournament,
        city,
        country,
        neutral,
    ):
        self.date = date

        self.home_team = home_team
        self.away_team = away_team

        self.home_score = home_score
        self.away_score = away_score

        self.tournament = tournament

        self.city = city
        self.country = country

        self.neutral = neutral

    @property
    def winner(self):
        if self.home_score > self.away_score:
            return self.home_team

        if self.away_score > self.home_score:
            return self.away_team

        return None

    @property
    def is_draw(self):
        return self.home_score == self.away_score

    def __str__(self):
        return (
            f"{self.home_team} "
            f"{self.home_score}-{self.away_score} "
            f"{self.away_team}"
        )