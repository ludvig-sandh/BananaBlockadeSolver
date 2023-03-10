from BananaBlockade.game_state import GameState
from heapq import heappush, heappop
from dataclasses import dataclass

@dataclass
class PQItem:
    distance: int
    estimate: int
    state: GameState

    def to_pair(self):
        return self.distance, self.state

    def __lt__(self, other):
        return self.distance + self.estimate < other.distance + other.estimate

class Solver:
    def __init__(self, starting_state: GameState):
        self.starting_state = starting_state

    def solve(self, verbal: bool = False):
        # A* search algorithm
        priority_queue = [PQItem(0, 0, self.starting_state)]
        visited = set()
        best_score = 1000000
        while len(priority_queue):
            front_item = heappop(priority_queue)
            distance, state = front_item.to_pair()

            if state in visited:
                continue
            visited.add(state)

            if state.is_won():
                return state, distance

            for neighbor_state in state.get_possible_moves():
                estimate = neighbor_state.heuristic_score()
                if distance + 1 + estimate < best_score and verbal:
                    best_score = distance + 1 + estimate
                    print("New best score:", best_score)
                heappush(priority_queue, PQItem(distance + 1, estimate, neighbor_state))