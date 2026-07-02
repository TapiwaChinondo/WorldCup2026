import sys

from data.download import load_matches

from teams.manager import TeamManager

from ratings.elo import EloRatingManager

from models.elo import EloPredictor
from models.historical import HistoricalPredictor
from models.poisson import PoissonPredictor
from models.random import RandomPredictor
from models.recent_form import RecentFormPredictor

from simulation.tournament import Tournament
from simulation.runner import SimulationRunner


def build_predictor(name, matches):
    if name == "historical":
        return HistoricalPredictor()

    if name == "recent":
        return RecentFormPredictor(number_of_matches=10)

    if name == "random":
        return RandomPredictor()

    if name == "elo":
        elo_manager = EloRatingManager()
        elo_manager.process_matches(matches)
        return EloPredictor(elo_manager)

    if name == "poisson":
        return PoissonPredictor(max_goals=6)

    raise ValueError(f"Unknown predictor: {name}")


def main():
    predictor_name = sys.argv[1] if len(sys.argv) > 1 else "elo"
    simulations = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

    matches = load_matches()

    manager = TeamManager(matches)
    predictor = build_predictor(predictor_name, matches)

    tournament = Tournament(manager, predictor)
    runner = SimulationRunner(tournament)

    results = runner.run(simulations)
    runner.print_results(results, simulations)


if __name__ == "__main__":
    main()