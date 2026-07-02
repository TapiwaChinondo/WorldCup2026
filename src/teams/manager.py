from teams.team import Team
from matches.match import Match

class TeamManager:

    def __init__(self, matches):
        self.teams = {}
        self.process_matches(matches)

    def get_team(self, name):
        if name not in self.teams:
            self.teams[name] = Team(name)

        return self.teams[name]

    def process_matches(self, matches):

        for _, row in matches.iterrows():

            if row[["home_score", "away_score"]].isna().any():
                continue

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

            home = self.get_team(match.home_team)
            away = self.get_team(match.away_team)

            home.add_match(
                match,
                match.home_score,
                match.away_score
            )

            away.add_match(
                match,
                match.away_score,
                match.home_score
            )
    
    def all_teams(self):
        return self.teams.values()
    
    def sorted_by_win_percentage(self):
        return sorted(
            self.teams.values(),
            key=lambda team: team.win_percentage,
            reverse=True
        )

    def __getitem__(self, name):
        return self.teams[name]