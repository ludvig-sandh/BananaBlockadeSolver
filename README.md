# BananaBlockadeSolver
An algorithm to solve [Banana Blockade](https://www.youtube.com/watch?v=jUVfdFLYqo0) levels from Wii Party. 
In Banana Blockade, you play on a grid that contains banana crates, boxes, obstacles and an exit.
The goal is to push the banana crates out through the exit before the time limit.
Both banana crates and regular boxes can be pushed and dragged around, in contrast to the other obstacles which are immovable.
Each level is configured differently - boxes, obstacles, and banana crates have different starting locations. 
In the actual game, there are additional 2x1 movable boxes in some levels that require two players to nudge. 
These are not implemented in my algorithm.

The [A-star search algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm) is used to quickly find a solution for a given level.
The heuristic function used to estimate a cost from a current game state to the solution is based on the following:
- The number of reachable walkable tiles: we want to maximise the reachable space (especially in the beginning so we can start interacting with the banana crates sooner)
- The number of banana crates left: the solution is found when this number is zero
- The summed manhattan distance between the bananas and the goal: The closer the banana crates are to the exit, the better

Here is a usage example:
```py
from BananaBlockade.game_state import GameState
from BananaBlockade.solver import Solver

starting_state = GameState("Level19.txt") # <- Path to level file
solver = Solver(starting_state)
finish_state, num_moves_needed = solver.solve()

print(num_moves_needed) #=> 37
```

Level19.txt - example level:
```
6 12
S..........#
..####.##..#
..#..OBO#..#
..#OBO..#..G
..##.####..#
...........#
```
In this level file, dots '.' represent empty tiles that can be walked on. 
'S' stands for Start and 'G' for Goal (exit). '#' are immovable obstacles and 'O' are movable moxes.
The first two integers specify the number of rows and columns of the level, respectively.

The GameState class has a history attribute that contains a copy of each game state from start to solution.
This way you can see the entire step of a solution.
