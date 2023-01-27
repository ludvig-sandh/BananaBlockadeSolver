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
            assert self.rows > 0 and self.cols > 0, "Number of rows and columns must be larger than zero"

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

    def __get_start_pos(self):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                if tile == TileType.START:
                    return (x, y)
        assert False, "No starting tile 'S' found"

    def __is_valid_pos(self, r, c):
        if r < 0 or c < 0:
            return False
        if r >= self.rows or c >= self.cols:
            return False
        if self.grid[r][c] in [TileType.OBSTACLE, TileType.BOX, TileType.BANANA]:
            return False
        return True

    def __count_reachable_tiles(self):
        # DFS from start tile
        stack = [self.__get_start_pos()]
        visited = set()
        while len(stack):
            current_tile = stack.pop()
            if current_tile in visited:
                continue
            visited.add(current_tile)
            r, c = current_tile

            deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for dr, dc in deltas:
                next_r, next_c = r + dr, c + dc
                if not self.__is_valid_pos(next_r, next_c):
                    continue
                stack.append((next_r, next_c))
        return len(visited)

    def __count_bananas_left(self):
        total = 0
        for row in self.grid:
            total += row.count(TileType.BANANA)
        return total

    def heuristic_score(self):
        bananas_left = self.__count_bananas_left()
        num_tiles = self.__count_reachable_tiles()
        return bananas_left * 20 + num_tiles

    def __repr__(self):
        # Concatenate all rows together
        return '\n'.join(self.grid)

    def __str__(self):
        return self.__repr__()