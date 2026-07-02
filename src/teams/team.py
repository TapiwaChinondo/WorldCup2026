class Team:

    def __init__(self, name):
        self.name = name

        self.matches = 0
        self.match_history = []

        self.wins = 0
        self.draws = 0
        self.losses = 0

        self.goals_for = 0
        self.goals_against = 0

    def add_match(self, match, goals_for, goals_against):
        self.match_history.append(match)

        self.matches += 1

        self.goals_for += goals_for
        self.goals_against += goals_against

        if goals_for > goals_against:
            self.wins += 1
        elif goals_for < goals_against:
            self.losses += 1
        else:
            self.draws += 1

    def last_matches(self, n):
        return self.match_history[-n:]

    def recent_goals_for_per_game(self, n=10):
        recent = self.last_matches(n)

        if not recent:
            return self.goals_per_game

        total = 0

        for match in recent:
            if match.home_team == self.name:
                total += match.home_score
            else:
                total += match.away_score

        return total / len(recent)

    def recent_goals_against_per_game(self, n=10):
        recent = self.last_matches(n)

        if not recent:
            return self.goals_against_per_game

        total = 0

        for match in recent:
            if match.home_team == self.name:
                total += match.away_score
            else:
                total += match.home_score

        return total / len(recent)

    def recent_win_percentage(self, n=10):
        recent = self.last_matches(n)

        if not recent:
            return self.win_percentage

        wins = 0

        for match in recent:
            if match.home_team == self.name:
                team_goals = match.home_score
                opponent_goals = match.away_score
            else:
                team_goals = match.away_score
                opponent_goals = match.home_score

            if team_goals > opponent_goals:
                wins += 1

        return wins / len(recent)

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    @property
    def win_percentage(self):
        if self.matches == 0:
            return 0.0

        return self.wins / self.matches

    @property
    def points(self):
        return self.wins * 3 + self.draws

    @property
    def goals_per_game(self):
        if self.matches == 0:
            return 0

        return self.goals_for / self.matches

    @property
    def goals_against_per_game(self):
        if self.matches == 0:
            return 0

        return self.goals_against / self.matches

    @property
    def draws_percentage(self):
        if self.matches == 0:
            return 0

        return self.draws / self.matches

    @property
    def losses_percentage(self):
        if self.matches == 0:
            return 0

        return self.losses / self.matches

    def __str__(self):
        return (
            f"{self.name}\n"
            f"Matches: {self.matches}\n"
            f"Wins: {self.wins}\n"
            f"Draws: {self.draws}\n"
            f"Losses: {self.losses}\n"
            f"Goals For: {self.goals_for}\n"
            f"Goals Against: {self.goals_against}\n"
            f"Goal Difference: {self.goal_difference}\n"
            f"Win %: {self.win_percentage:.2%}\n"
            f"Goals/Game: {self.goals_per_game:.2f}\n"
            f"Goals Against/Game: {self.goals_against_per_game:.2f}\n"
            f"Recent Goals/Game: {self.recent_goals_for_per_game():.2f}\n"
            f"Recent Goals Against/Game: {self.recent_goals_against_per_game():.2f}\n"
            f"Recent Win %: {self.recent_win_percentage():.2%}"
        )