from BananaBlockade.game_state import GameState
from BananaBlockade.solver import Solver
import sys

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Must specify second argument: map file"
    map_file_path = sys.argv[1]
    state = GameState(map_file_path)
    solver = Solver(state)
    solution = solver.solve()
    
    finish_state, finish_distance = solution
    
    print("All moves to solution:")
    for state in finish_state.history:
        print(state, end="\n\n")
    print(finish_state)

    print("Number of moves needed for solution:", finish_distance)
