class Tournament:

    def __init__(self, manager, predictor):
        self.manager = manager
        self.predictor = predictor

    def play_round(self, fixtures, round_name, randomize=False, verbose=True):
        if verbose:
            print(f"\n{round_name}\n")

        winners = []

        for team_a_name, team_b_name in fixtures:
            team_a = self.manager[team_a_name]
            team_b = self.manager[team_b_name]

            prediction = self.predictor.predict(team_a, team_b)

            if randomize:
                winner = prediction.sample_winner()
            else:
                winner = prediction.winner

            winners.append(winner.name)

            if verbose:
                print(
                    f"{team_a.name} vs {team_b.name} -> "
                    f"{winner.name}"
                )

        return winners

    def simulate(self, randomize=False, verbose=True):
        round_of_32 = [
            ("South Africa", "Canada"),
            ("Brazil", "Japan"),
            ("Germany", "Paraguay"),
            ("Netherlands", "Morocco"),
            ("Ivory Coast", "Norway"),
            ("France", "Sweden"),
            ("Mexico", "Ecuador"),
            ("England", "DR Congo"),
            ("Belgium", "Senegal"),
            ("United States", "Bosnia and Herzegovina"),
            ("Spain", "Austria"),
            ("Portugal", "Croatia"),
            ("Switzerland", "Algeria"),
            ("Australia", "Egypt"),
            ("Argentina", "Cape Verde"),
            ("Colombia", "Ghana"),
        ]

        r32_winners = self.play_round(round_of_32, "Round of 32",  randomize=randomize,  verbose=verbose)

        round_of_16 = [
            (r32_winners[0], r32_winners[3]),
            (r32_winners[2], r32_winners[5]),
            (r32_winners[1], r32_winners[4]),
            (r32_winners[6], r32_winners[7]),
            (r32_winners[11], r32_winners[10]),
            (r32_winners[9], r32_winners[8]),
            (r32_winners[14], r32_winners[13]),
            (r32_winners[12], r32_winners[15]),
        ]

        r16_winners = self.play_round(round_of_16, "Round of 16",  randomize=randomize, verbose=verbose)

        quarterfinals = [
            (r16_winners[1], r16_winners[0]),
            (r16_winners[4], r16_winners[5]),
            (r16_winners[2], r16_winners[3]),
            (r16_winners[6], r16_winners[7]),
        ]

        qf_winners = self.play_round(quarterfinals, "Quarterfinals",  randomize=randomize, verbose=verbose)

        semifinals = [
            (qf_winners[0], qf_winners[1]),
            (qf_winners[2], qf_winners[3]),
        ]

        sf_winners = self.play_round(semifinals, "Semifinals",  randomize=randomize, verbose=verbose)

        final = [
            (sf_winners[0], sf_winners[1])
        ]

        champion = self.play_round(final, "Final",  randomize=randomize, verbose=verbose)[0]

        print(f"\nChampion: {champion}")
        
        return champion