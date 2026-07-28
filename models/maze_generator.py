"""Maze Generator class for the A-Maze-ing project.

This module provides the Maze Generator class to create and carve
the maze structure. As well as generate the path between the maze's
entry and exit.
"""


from . import Maze, Cell
from collections import deque
import random


class MazeGenerator:
    """Generates maze structures.

    Responsible for initializing the grid, placing the entrance and exit,
    carving passages, and building solvable maze layouts using search-based
    algorithms.
    """
    def __init__(
        self,
        width: int,
        height: int,
        entry_x: int,
        entry_y: int,
        exit_x: int,
        exit_y: int,
        perfect: bool = True,
        seed: int | None = None,
        animation: bool = False,
     ) -> None:
        """Initialize the Maze Generation Class with default state."""
        self.width = width
        self.height = height
        self.entry_x = entry_x
        self.entry_y = entry_y
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.perfect = perfect
        self.seed = seed
        self.animation = animation
        self.rng = random.Random(seed)

        self._validate_entry_exit()

        self.entry: Cell = Cell(x=entry_x, y=entry_y, walls=15, entrance=True)
        self.exit: Cell = Cell(x=exit_x, y=exit_y, walls=15, entrance=True)

        self.maze = Maze(
            width=width,
            height=height,
            entry=self.entry,
            exit=self.exit,
        )

        self.solutions: list[list[Cell]] = []

    def maze_init(self) -> None:
        """Initialize the maze grid with fresh cells.

        Creates a two-dimensional grid of cells using the configured width and
        height, assigns the entrance and exit cells, marks them in the grid,
        and applies the static "42" pattern in the center of the maze.
        """
        self.maze.grid = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                cell: Cell = Cell(x=x, y=y)
                row.append(cell)
            self.maze.grid.append(row)
        self.entry = self.maze.grid[self.entry_y][self.entry_x]
        self.exit = self.maze.grid[self.exit_y][self.exit_x]
        if self.entry is None or self.exit is None:
            raise ValueError("Error: Entry and Exit cannot be None.")
        self.entry.entrance = True
        self.exit.exit = True
        self._validate_entry_exit()
        if self.width < 9 or self.height < 6:
            print("Error: Maze size is too small for '42' pattern.")
        else:
            self.draw_fortytwo()

    def draw_fortytwo(self) -> None:
        """Draws the static "42" pattern in the center of the maze.

        Raises an error if entry or exit haven't been initialized
        and prints a warning message if the maze is two small to apply
        the "42" pattern.
        """
        if self.entry is None or self.exit is None:
            raise ValueError("Entry/exit must be "
                             "initialized before draw_fortytwo().")

        if self.width < 9 or self.height < 6:
            print("Error: Maze size is too small for '42' pattern.")

        offset_x: int = (self.width - 9) // 2
        offset_y: int = max(1, (self.height - 5) // 2)

        pattern_42: list[str] = [
            ".#...###.",
            ".#.....#.",
            ".###.###.",
            "...#.#...",
            "...#.###.",
        ]

        for rel_y, row in enumerate(pattern_42):
            for rel_x, char in enumerate(row):
                if char != '#':
                    continue

                tx, ty = offset_x + rel_x, offset_y + rel_y

                if (
                    (self.entry.x == tx
                     and self.entry.y == ty)
                    or (self.exit.x == tx
                        and self.exit.y == ty)
                ):
                    raise ValueError('Entry & Exit '
                                     'must not be in 42 position.')
                self.maze.grid[ty][tx].walls = 15
                self.maze.grid[ty][tx].static = True
                self.maze.grid[ty][tx].visited = True

    def _validate_entry_exit(self) -> None:
        """
        Validates that entry and exit are within maze bounds
        and they do not share the same coordinates.
        """
        if not (0 <= self.entry_x < self.width
                and 0 <= self.entry_y < self.height):
            raise ValueError("Entry is out of bounds.")
        if not (0 <= self.exit_x < self.width
                and 0 <= self.exit_y < self.height):
            raise ValueError("Exit is out of bounds.")
        if (self.entry_x == self.exit_x
                and self.entry_y == self.exit_y):
            raise ValueError("Entry and exit must be different.")

    def reset_visited(self) -> None:
        """Resets non-static visited cells."""
        for row in self.maze.grid:
            for cell in row:
                if not getattr(cell, "static", False):
                    cell.visited = False

    def carve_entrance_exit(self):
        """Makes entry and exit accesible."""
        self.do_carve(self.entry, "Entry")
        self.do_carve(self.exit, "Exit")

    def do_carve(self, cell: Cell, label: str = "cell") -> None:
        """Carves an entrance to a chosen cell.

        Raises an error if the cell is placed within the "42" pattern.
        Checks its neighbours and randomly picks one to remove the wall
        between them. Making the original cell accesible.
        """
        x, y = cell.x, cell.y
        original_cell: Cell = self.maze.grid[y][x]

        if getattr(original_cell, "static", False):
            raise ValueError(f"{label} cannot be placed on the 42 pattern.")

        neighbours = self.get_all_neighbours(original_cell)
        if not neighbours:
            raise ValueError(f"{label} has no valid neighbours to carve.")
        n_cell = self.rng.choice(neighbours)
        self.remove_walls(original_cell, n_cell)

    def get_all_neighbours(self, cell: Cell) -> list[Cell]:
        """Provides a list of non-static neighbouring cells.

        It checks the four sides of the input cell and returns a list
        of non-static neighbouring cells which are placed within
        maze's bounds.

        Parameter:
            cell: Cell
        Returns:
            list[Cell]
        """
        neighbours: list[Cell] = []
        if cell.y > 0:
            up = self.maze.grid[cell.y-1][cell.x]
            if not getattr(up, "static", False):
                neighbours.append(up)
        if cell.y < self.maze.height - 1:
            down = self.maze.grid[cell.y+1][cell.x]
            if not getattr(down, "static", False):
                neighbours.append(down)
        if cell.x > 0:
            west = self.maze.grid[cell.y][cell.x - 1]
            if not getattr(west, "static", False):
                neighbours.append(west)
        if cell.x < self.maze.width - 1:
            east = self.maze.grid[cell.y][cell.x + 1]
            if not getattr(east, "static", False):
                neighbours.append(east)
        return neighbours

    def get_unvisited_neighbours(self, cell: Cell) -> list[Cell]:
        """Provides a list of non-static unvisited neighbouring cells.

        It checks the four sides of the input cell and returns a list
        of non-static unvisited neighbouring cells which are placed within
        maze's bounds.

        Parameter:
            cell: Cell
        Returns:
            list[Cell]
        """
        neighbours: list[Cell] = []
        if cell.y > 0:
            up = self.maze.grid[cell.y-1][cell.x]
            if not up.visited and not getattr(up, "static", False):
                neighbours.append(up)

        if cell.y < self.maze.height - 1:
            down = self.maze.grid[cell.y+1][cell.x]
            if not down.visited and not getattr(down, "static", False):
                neighbours.append(down)

        if cell.x > 0:
            west = self.maze.grid[cell.y][cell.x - 1]
            if not west.visited and not getattr(west, "static", False):
                neighbours.append(west)

        if cell.x < self.maze.width - 1:
            east = self.maze.grid[cell.y][cell.x + 1]
            if not east.visited and not getattr(east, "static", False):
                neighbours.append(east)
        return neighbours

    def get_reachable_neighbours(self, cell: Cell) -> list[Cell]:
        """Provides a list of non-static unvisited accesible
        neighbouring cells.

        It checks the four sides of the input cell and returns a list
        of non-static unvisited accesible neighbouring cells which
        are placed within maze's bounds.
        Accesible meaning cell's are not separated by a wall.

        Parameter:
            cell: Cell
        Returns:
            list[Cell]
        """
        neighbours: list[Cell] = []
        if cell.y > 0:
            up = self.maze.grid[cell.y - 1][cell.x]
            if (not up.visited and not self._has_wall_between(cell, up)
                    and not getattr(up, "static", False)):
                neighbours.append(up)

        if cell.y < self.maze.height - 1:
            down = self.maze.grid[cell.y + 1][cell.x]
            if (not down.visited and not self._has_wall_between(cell, down)
                    and not getattr(down, "static", False)):
                neighbours.append(down)

        if cell.x > 0:
            west = self.maze.grid[cell.y][cell.x - 1]
            if (not west.visited and not self._has_wall_between(cell, west)
                    and not getattr(west, "static", False)):
                neighbours.append(west)

        if cell.x < self.maze.width - 1:
            east = self.maze.grid[cell.y][cell.x + 1]
            if (not east.visited and not self._has_wall_between(cell, east)
                    and not getattr(east, "static", False)):
                neighbours.append(east)
        return neighbours

    NORTH = 1  # 001
    EAST = 2   # 010
    SOUTH = 4  # 010
    WEST = 8   # 100
    ALL = 15   # 1111

    def _has_wall_between(self, cell_a: Cell, cell_b: Cell) -> bool:
        """Checks if two cells are separated by a wall.

        ValueError raises if the cells provided are not neighbours.

        Parameters:
            cell_a: Cell
            cell_b: Cell
        Returns:
            boolean
        """
        dx = cell_b.x - cell_a.x
        dy = cell_b.y - cell_a.y

        if dx == 1:
            return (cell_a.walls & self.EAST) != 0

        elif dx == -1:
            return (cell_a.walls & self.WEST) != 0

        elif dy == 1:
            return (cell_a.walls & self.SOUTH) != 0

        elif dy == -1:
            return (cell_a.walls & self.NORTH) != 0

        raise ValueError("Cells are not neighbours has wall")

    def remove_walls(self, cell_a: Cell, cell_b: Cell) -> None:
        """Removes the wall separating two cells.
        ValueError raises if the cells provided are not neighbours.

        Parameters:
            cell_a: Cell
            cell_b: Cell
        """
        dx = cell_b.x - cell_a.x
        dy = cell_b.y - cell_a.y

        if dx == 1:
            cell_a.walls &= ~self.EAST
            cell_b.walls &= ~self.WEST

        elif dx == -1:
            cell_a.walls &= ~self.WEST
            cell_b.walls &= ~self.EAST

        elif dy == 1:
            cell_a.walls &= ~self.SOUTH
            cell_b.walls &= ~self.NORTH

        elif dy == -1:
            cell_a.walls &= ~self.NORTH
            cell_b.walls &= ~self.SOUTH

    def dfs_generate(self) -> list[list[Cell]]:
        """Main path generation function.
        1. It generates the path patterns of the Maze Grid using DFS algorithm.
        2. Ensures full connectivity within the maze so there are not
        isolated areas.

        PERFECT=FALSE
        If the maze's config file specifies PERFECT=FALSE the following rules
        apply to this function:
        1. Pacman check: Ensure four corners and center are accesible.
        2. Two paths: Ensure there are at least two different
            paths from entry to exit.
        3. Reduce dead ends: Ensure there are a maximum of two
            dead-ends within the maze grid.

        Return = Maze Grid
        """
        self._generate_maze_dfs()
        self._connectivity()

        if not self.perfect:
            self._pacman_check()
            attempts = 0
            while not self._two_paths() and attempts < 10:
                self._create_multiple_paths()
                attempts += 1
            self._reduce_dead_end()
            dead_ends: list[Cell] = self._count_dead_ends()
            attempts = 0
            while len(dead_ends) < 5 and len(dead_ends) > 0 and attempts < 60:
                self._reduce_five_ends()
                attempts += 1

        return self.maze.grid

    def _generate_maze_dfs(self) -> None:
        """Carves paths within the maze grid.
        Starting at the entry cell and using DFS algorithm checks
        unvisited neighbours and randomly removes the walls that
        separates them.

        Raises ValueError if entry has not been inicialized.
        """
        if self.entry is None:
            raise ValueError("Error: self.entry must be inicialized"
                             " before generating the maze.")
        start = self.entry
        stack = []
        stack.append(start)
        start.visited = True

        while len(stack) > 0:
            current = stack[-1]
            neighbours = self.get_unvisited_neighbours(current)
            if len(neighbours) > 0:
                nxt = self.rng.choice(neighbours)
                self.remove_walls(current, nxt)
                nxt.visited = True
                stack.append(nxt)
            else:
                stack.pop()

    def _create_multiple_paths(self) -> None:
        """Carves multiple paths within the maze grid.
        Function used in a non perfect Maze.

        Starting at a randomly chosen cell checks
        unvisited neighbours and removes the wall that
        separates the cell with its randomly chose neighbour.
        """
        for _ in range(15):
            y: int = self.rng.randint(0, self.height - 1)
            x: int = self.rng.randint(0, self.width - 1)
            cell = self.maze.grid[y][x]
            neighbours = self.get_all_neighbours(cell)
            if not neighbours:
                continue
            nb = self.rng.choice(neighbours)
            if self._has_wall_between(cell, nb):
                self.remove_walls(cell, nb)

    def _two_paths(self) -> bool:
        """Checks if there are two possible paths from entry
        to exit within the maze grid.

        Raises ValueError if entry/exit has not been inicialized.
        Returns a boolean value.
        """
        if self.entry is None:
            raise ValueError("Error: self.entry must be "
                             "initialized before two paths")

        first_path = self.solve_maze_dfs(self.entry, self.exit)
        if not first_path:
            return False

        for cell in first_path:
            if cell == self.entry or cell == self.exit:
                continue
            second_path = self.solve_maze_dfs(cell, self.exit)
            if second_path:
                return True

        return False

    def _connectivity(self) -> None:
        """Ensures full connectivity throughout the maze grid, meaning
        that all cells are accesible and there are not any blocked
        areas.

        1. Builds a main path from self.entry to other accesible neighbours.
        2. Checks whether there are any non static cells within the maze
        that are not included in the main path.
        3. Loops through each cell not included in main_path to carve
        alternative paths that reach them.

        Raises ValueError if entry/exit has not been inicialized.
        """
        if self.entry is None or self.exit is None:
            raise ValueError("Error: self.entry and self.exit must"
                             "be inicialized before connectivity")
        main_path = self._flood_maze(self.entry)

        while self._transit_cell(main_path) is True:
            start: Cell | None = self._first_transit_cell(main_path)
            if start is not None:
                next_component = self._flood_maze(start)
                wall_found: bool = False

                for cell_a in next_component:
                    for cell_b in self.get_all_neighbours(cell_a):
                        if cell_b in main_path:
                            self.remove_walls(cell_a, cell_b)
                            wall_found = True
                        if wall_found:
                            break
                    if wall_found:
                        break
                if not wall_found:
                    break
                main_path = self._flood_maze(self.entry)

    def _transit_cell(self, main_path: list[Cell]) -> bool:
        """Searches within the maze grid non static cells which
        are not included in the given path.
        Returns True as long as there are non static cells within the maze grid
        that are not included in the main path.

        Parameters:
            main_path: list[Cell]
        Returns:
            boolean
        """
        for row in self.maze.grid:
            for cell in row:
                if cell.static is not True and cell not in main_path:
                    return True
        return False

    def _first_transit_cell(self, main_path: list[Cell]) -> Cell | None:
        """Searches within the maze grid non static cells which
        are not included in the given path.
        Returns the first non static cell not included in the main path.

        Parameters:
            main_path: list[Cell]
        Returns:
            Cell | None
        """
        for row in self.maze.grid:
            for cell in row:
                if cell.static is not True and cell not in main_path:
                    return cell
        return None

    def _flood_maze(self, start: Cell) -> list[Cell]:
        """Makes a given cell accesible by building a path
        from the parameter path to any unvisited neighbours,
        using the BFS algorithm.

        Parameters:
            start: Cell
        Returns:
            list[Cell]
        """
        self.reset_visited()
        queue = deque([start])
        start.visited = True
        path: list[Cell] = []

        while len(queue) > 0:
            current = queue.popleft()
            path.append(current)
            neighbours = self.get_reachable_neighbours(current)
            for n in neighbours:
                if not n.visited:
                    n.visited = True
                    queue.append(n)
        return path

    def _pacman_check(self) -> None:
        """Ensures that the maze grid's four edge corners and center
        are accesible.
        It loops through each corners and builds a path using the
        BFS algorithm.
        """
        for corner in [self.maze.grid[0][0], self.maze.grid[0][self.width - 1],
                       self.maze.grid[self.height - 1][0],
                       self.maze.grid[self.height - 1][self.width - 1],
                       self.maze.grid[self.height // 2][self.width // 2]]:
            if self.solve_maze_bfs(self.entry, corner):
                continue

            for n in self.get_all_neighbours(corner):
                if self.solve_maze_bfs(self.entry, n):
                    self.remove_walls(n, corner)
                    break

    def _reduce_dead_end(self) -> None:
        """Reduces the number of dead ends within the maze grid.

        1. Counts how many dead ends exist in the grid.
        2. Chooses a random dead end cell
        3. Checks all its neighbours and selects those who
        share a wall.
        4. Randomly picks one of the neighbours and destroys
        their sharing wall.

        Tries to reduce dead ends to max of 2 during 1000 attemps.
        """
        attempts: int = 0

        while attempts < 2000:
            dead_ends: list[Cell] = self._count_dead_ends()
            if len(dead_ends) <= 2:
                break

            cell = self.rng.choice(dead_ends)
            neighbours = self.get_all_neighbours(cell)

            candidates: list[Cell] = []
            for n in neighbours:
                if self._has_wall_between(cell, n):
                    candidates.append(n)

            if not candidates:
                continue

            nb: Cell = self.rng.choice(candidates)
            self.remove_walls(cell, nb)
            attempts += 1

    def _reduce_five_ends(self) -> None:
        """Auxiliary function which aims to reduce the number of dead ends
        from a list of five cells.

        Loops through each dead end and picks the neighbours which share
        a wall. Then randomly picks a candidate and breaks the wall they share.
        """
        dead_ends: list[Cell] = self._count_dead_ends()
        for cell in dead_ends:
            neighbours = self.get_all_neighbours(cell)
            candidates: list[Cell] = []
            for n in neighbours:
                if self._has_wall_between(cell, n):
                    candidates.append(n)
            if not candidates:
                continue

            nb: Cell = self.rng.choice(candidates)
            self.remove_walls(cell, nb)

    def _count_dead_ends(self) -> list[Cell]:
        """Counts how many dead end cells exist within the
        maze grid.
        For each cell within the maze it check if it only has
        one open wall.

        Returns:
            list[Cell].
        """
        dead_ends: list[Cell] = []

        for row in self.maze.grid:
            for cell in row:
                if getattr(cell, "static", False):
                    continue

                open_paths: int = 0
                for n in self.get_all_neighbours(cell):
                    if not self._has_wall_between(cell, n):
                        open_paths += 1

                if open_paths == 1:
                    dead_ends.append(cell)

        return dead_ends

    def solve_maze_bfs(self, start: Cell, end: Cell) -> list[Cell]:
        """Solver function that provides the path from one start cell
        to the end cell using the BFS algorithm.

        Raises ValueError if start/end has not been inicialized.

        Parameters:
            start: Cell
            end: Cell
        Returns:
            list[Cell] | []
        """
        if start is None or end is None:
            raise ValueError("Error: start and end must"
                             "be inicialized before solve bfs")
        self.reset_visited()
        queue = deque([start])
        start.visited = True
        parents: dict[Cell, Cell] = {}

        while len(queue) > 0:
            current = queue.popleft()
            if current == end:
                return self.reconstruct_path(end, parents)
            neighbours = self.get_reachable_neighbours(current)
            for n in neighbours:
                if not n.visited:
                    n.visited = True
                    parents[n] = current
                    queue.append(n)
        return []

    def solve_maze_dfs(self, start: Cell, end: Cell |
                       None = None) -> list[Cell]:
        """Solver function that provides the path from one start cell
        to the end cell using the DFS algorithm.

        Raises ValueError if start/end has not been inicialized.
        Parameters:
            start: Cell
            end: Cell
        Returns:
            list[Cell] | []
        """
        if start is None or end is None:
            raise ValueError("Error: start and end must"
                             "be inicialized before solve dfs")

        self.reset_visited()

        stack = [start]
        parents: dict[Cell, Cell] = {}
        start.visited = True

        while stack:
            current = stack.pop()
            if current == end:
                return self.reconstruct_path(end, parents)
            neighbours = self.get_reachable_neighbours(current)
            for n in neighbours:
                if not n.visited:
                    n.visited = True
                    parents[n] = current
                    stack.append(n)

        return []

    def reconstruct_path(self,
                         end: Cell,
                         parents: dict[Cell, Cell]) -> list[Cell]:
        """Converts a dictionary of cells into a list of cells that
        represent the path from starting cell to an end cell.

        Parameters:
            end: Cell
            parents: dict[Cell, Cell] = dictionary of neighbouring cells
        Returns:
            list[Cell]
        """
        if end is None:
            raise ValueError("Error: end must be inicialized before"
                             "reconstructing the path.")
        path: list[Cell] = [end]
        current = end
        while current in parents:
            current = parents[current]
            path.append(current)
        path.reverse()
        return path
