from BananaBlockade.game_state import GameState
import sys

if __name__ == "__main__":
    assert len(sys.argv) == 2, "Must specify second argument: map file"
    map_file_path = sys.argv[1]
    state = GameState(map_file_path)
    print(state.heuristic_score())