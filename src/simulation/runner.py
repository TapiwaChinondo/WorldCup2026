from collections import Counter


class SimulationRunner:

    def __init__(self, tournament):
        self.tournament = tournament

    def run(self, number_of_simulations):
        champions = Counter()

        for _ in range(number_of_simulations):
            champion = self.tournament.simulate(
                randomize=True,
                verbose=False
            )

            champions[champion] += 1

        return champions

    def print_results(self, champions, number_of_simulations):
        print(f"\nResults after {number_of_simulations} simulations\n")

        for team, count in champions.most_common():
            probability = count / number_of_simulations

            print(f"{team:<20} {probability:.2%}")