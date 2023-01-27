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

    def __init__(self, from_file_path: str = None, grid: List[str] = None):
        self.history = []
        if from_file_path is not None:
            self.__load_file(from_file_path)
            return

        assert grid is not None, "GameState object requires at least one argument"

        # Make a copy of grid
        self.grid = []
        for row in grid:
            self.grid.append(''.join(row))
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        
    def __load_file(self, from_file_path):
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
        for r, row in enumerate(self.grid):
            for c, tile in enumerate(row):
                if tile == TileType.START:
                    return (r, c)
        assert False, "No starting tile 'S' found"
        
    def __get_goal_pos(self):
        for r, row in enumerate(self.grid):
            for c, tile in enumerate(row):
                if tile == TileType.GOAL:
                    return (r, c)
        assert False, "No ending tile 'G' found"

    def __is_valid_pos(self, r, c):
        if r < 0 or c < 0:
            return False
        if r >= self.rows or c >= self.cols:
            return False
        return True
    
    def __is_walkable_pos(self, r, c):
        return self.grid[r][c] not in [TileType.OBSTACLE, TileType.BOX, TileType.BANANA]

    def __get_reachable_tiles(self):
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
                if not self.__is_walkable_pos(next_r, next_c):
                    continue
                stack.append((next_r, next_c))
        return list(visited)

    def __count_reachable_tiles(self):
        return len(self.__get_reachable_tiles())

    def __count_bananas_left(self):
        total = 0
        for row in self.grid:
            total += row.count(TileType.BANANA)
        return total

    def __get_movable_neighbors(self, r, c):
        neighbors = []
        deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dr, dc in deltas:
            box_r, box_c = r + dr, c + dc
            if not self.__is_valid_pos(box_r, box_c):
                continue
            if self.grid[box_r][box_c] in [TileType.BOX, TileType.BANANA]:
                neighbors.append((box_r, box_c))
        return neighbors

    def get_copy(self):
        copied = GameState(grid=self.grid)
        for grid in self.history:
            copied.history.append(grid)
        return copied

    def __get_tile(self, tile_rc):
        return self.grid[tile_rc[0]][tile_rc[1]]

    def __set_tile(self, tile_rc, tile_type):
        row = list(self.grid[tile_rc[0]])
        row[tile_rc[1]] = tile_type
        self.grid[tile_rc[0]] = ''.join(row)

    def __can_move_box(self, from_tile, to_tile):
        if not self.__is_valid_pos(*from_tile):
            return False
        if not self.__is_valid_pos(*to_tile):
            return False
        if not self.__is_walkable_pos(*to_tile):
            return False

        if self.__get_tile(from_tile) not in [TileType.BOX, TileType.BANANA]:
            return False

        if self.__get_tile(from_tile) == TileType.BOX:
            if self.__get_tile(to_tile) == TileType.GOAL:
                return False
        
        if self.__get_tile(to_tile) not in [TileType.EMPTY, TileType.GOAL]:
            return False
        
        return True

    def __add_to_history(self):
        self.history.append(self.get_copy())

    def __move_box(self, from_tile, to_tile):
        # Remember last state
        self.__add_to_history()

        # Assume it's possible to move a box from from_tile to to_tile
        if self.__get_tile(from_tile) == TileType.BANANA:
            if to_tile != self.__get_goal_pos():
                self.__set_tile(to_tile, TileType.BANANA)
            self.__set_tile(from_tile, TileType.EMPTY)
        elif self.__get_tile(from_tile) == TileType.BOX:
            self.__set_tile(to_tile, TileType.BOX)
            self.__set_tile(from_tile, TileType.EMPTY)
    
    def get_possible_moves(self):
        # Returns a list of GameState instances
        possible = []

        reachable_tiles = self.__get_reachable_tiles()
        tiles_next_to_boxes = []
        for r, c in reachable_tiles:
            box_tiles = self.__get_movable_neighbors(r, c)
            for box_tile in box_tiles:
                box_r, box_c = box_tile
                dr, dc = box_r - r, box_c - c
                
                # Alternative 1: push box
                box_next_tile = box_r + dr, box_c + dc
                if self.__can_move_box(box_tile, box_next_tile):
                    possible_state = self.get_copy()
                    possible_state.__move_box(box_tile, box_next_tile)
                    possible.append(possible_state)

                # Alternative 2: pull box
                box_next_tile = r, c
                stand_next_tile = r - dr, c - dc
                if not self.__is_valid_pos(r - dr, c - dc):
                    continue
                if not self.__is_walkable_pos(r - dr, c - dc):
                    continue
                if not self.__can_move_box(box_tile, box_next_tile):
                    continue
                possible_state = self.get_copy()
                possible_state.__move_box(box_tile, box_next_tile)
                possible.append(possible_state)
        return possible

    def __count_total_banana_dist(self):
        total = 0
        for row_index, row in enumerate(self.grid):
            for col_index, tile in enumerate(row):
                if tile == TileType.BANANA:
                    goal = self.__get_goal_pos()
                    dr = abs(goal[0] - row_index)
                    dc = abs(goal[1] - col_index)
                    total += dr + dc
        return total

    def heuristic_score(self):
        bananas_left = self.__count_bananas_left()
        num_tiles = self.__count_reachable_tiles()
        banana_dist = self.__count_total_banana_dist()
        return bananas_left * 20 + banana_dist * 5 - num_tiles

    def is_won(self):
        return self.__count_bananas_left() == 0

    def __repr__(self):
        # Concatenate all rows together
        return '\n'.join(self.grid)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        total = 0
        prime = 31
        int64_limit = 2 ** 64 - 1
        for row_index, row in enumerate(self.grid):
            for col_index, tile in enumerate(row):
                tile_index = row_index + col_index
                total += (ord(tile) * prime ** tile_index) % int64_limit
        return total

    def __eq__(self, other):
        return hash(self) == hash(other)