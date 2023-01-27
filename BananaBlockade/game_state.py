from typing import List

class TileType:
    EMPTY = '.'
    OBSTACLE = '#'
    BOX = 'O'
    BANANA = 'B'
    START = 'S'
    GOAL = 'G'

    TYPES = '.#OBSG'

class GameState:

    def __init__(self, from_file_path: str):
        # Read input from file
        with open(from_file_path, 'r') as f:
            lines = f.read().split("\n")
            self.rows, self.cols = [int(i) for i in lines[0].split()]
            assert (self.rows > 0, self.cols > 0), "Number of rows and columns must be larger than zero"

            last_row_index = len(lines)
            if '' in lines: 
                last_row_index = lines.index('')
            grid_lines = lines[1:last_row_index]

            # Some error checking
            assert self.rows == last_row_index - 1, "Number of rows must be at least one"
            assert all(len(line) == self.cols for line in grid_lines), "Empty line"
            assert all(len(line) == self.cols for line in grid_lines), "All rows must have equal length"
            
            # Build starting game grid state
            self.__build_grid(grid_lines)

    def __build_grid(self, grid_lines: List[str]):
        self.grid = []
        for row_index, line in enumerate(grid_lines):
            for col_index, tile in enumerate(line):
                assert tile in TileType.TYPES, f"Unrecognized tile {tile} at row {row_index}, column {col_index}"
            self.grid.append(line)

    def __repr__(self):
        # Concatenate all rows together
        return '\n'.join(self.grid)

    def __str__(self):
        return self.__repr__()