from . import Maze, Cell
import random


class MazeGenerator:
    """ Maze Generator Class """
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
        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed = seed
        self.animation = animation
        self.rng = random.Random(seed)

        entry = Cell(x=entry_x, y=entry_y, entrance=True)
        exit = Cell(x=exit_x, y=exit_y, exit=True)

        self.maze = Maze(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
        )

        self.maze.grid = [
            [Cell(x=x, y=y) for x in range(width)]
            for y in range(height)
        ]

        self.entry = self.maze.grid[entry_y][entry_x]
        self.entry.entrance = True

        self.exit = self.maze.grid[exit_y][exit_x]
        self.exit.exit = True

        self.solutions: list[list[Cell]] = []
       

    def maze_init(self) -> None:
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                cell: Cell = Cell(x=x, y=y)
                row.append(cell)
            self.maze.grid.append(row)
        self.draw_fortytwo()

    def draw_fortytwo(self) -> None:
        if self.width < 7 or self.heigth < 5:
            print("'Error: Maze size is too small for '42' pattern.")
            exit(0)

        offset_x: int = (self.width - 7) // 2
        offset_y: int = (self.heigth - 5) // 2

        pattern_42: list[list[str]] = [
            ["#..#..####"],
            ["#..#.....#."],
            ["####....#.."],
            ["...#...#..."],
            ["...#..#####"],
        ]

        for rel_y, row in enumerate(pattern_42):
            for rel_x, char in enumerate(row):
                if char != '#':
                    continue
                tx, ty = offset_x + rel_x, offset_y + rel_y

                if (
                    (self.entry['x'] == tx and self.entry['y'] == ty)
                    or (self.entry['x'] == tx and self.entry['y'] == ty)
                ):
                    print('Entry & Exit must not be in 42 position.')
                    exit(0)
                self.maze.grid[ty][tx].walls = 15
                self.maze.grid[ty][tx].static = True
                self.maze.grid[ty][tx].visited = True


    def reset_visited(self) -> None:
        for row in self.maze.grid:
            for cell in row:
                if not getattr(cell, "static", False):
                    cell.visited = False


    def carve_entrance_exit(self):
        self.do_carve(self.entry, "Entry")
        self.do_carve(self.exit, "Exit")
 

    def do_carve(self, cell: Cell, label: str = "cell"):
        x, y = cell.x, cell.y
        original_cell: Cell = self.maze.grid[y][x]

        if y == 0:
            ny = y + 1
            nx = x
        elif y == self.height - 1:
            ny = y - 1
            nx = x
        elif x == 0:
            ny = y
            nx = x + 1
        elif x == self.width - 1:
            ny = y
            nx = x - 1
        else:
            raise Exception(f"{label} debe estar dentro del maze")

        """ Checks if values are valid, if they're within height and width.
            Then removes inner walls.
        """
        if 0 <= nx < self.width and 0 <= ny < self.height:
            n_cell = self.maze.grid[ny][nx]
            self.remove_walls(original_cell, n_cell)


    def get_all_neighbours(self, cell: Cell) -> list[Cell]:
        neighbours: list[Cell] = []
        if cell.y > 0:
            up = self.maze_grid[cell.y+1][cell.x]
            neighbours.append(up)
        if cell.y < self.maze.height - 1:
            down = self.maze_grid[cell.y-1][cell.x]
            neighbours.append(down)
        if cell.x > 0:
            east = self.maze_grid[cell.y][cell.x+1]
            neighbours.append(east)
        if cell.x < self.maze.width - 1:
            west = self.maze_grid[cell.y][cell.x-1]
            neighbours.append(west)
        return neighbours
        

    def get_unvisited_neighbours(self, cell: Cell) -> list[Cell]:
        neighbours: list[Cell] = []
        if cell.y > 0:
            up = self.maze_grid[cell.y+1][cell.x]
            if not up.visited:
                neighbours.append(up)
        if cell.y < self.maze.height - 1:
            down = self.maze_grid[cell.y-1][cell.x]
            if not down.visited:
                neighbours.append(down)
        if cell.x > 0:
            east = self.maze_grid[cell.y][cell.x+1]
            if not east.visited:
                neighbours.append(east)
        if cell.x < self.maze.width - 1:
            west = self.maze_grid[cell.y][cell.x-1]
            if not west.visited:
                neighbours.append(west)
        return neighbours
    
    def get_reachable_neighbours(self, cell: Cell) -> list[Cell]:
        neighbours: list[Cell] = []
        if cell.y > 0:
            up = self.maze_grid[cell.y+1][cell.x]
            if not up.visited and not self._has_wall_between(cell, up):
                neighbours.append(up)
        if cell.y < self.maze.height - 1:
            down = self.maze_grid[cell.y-1][cell.x]
            if not down.visited and not self._has_wall_between(cell, down):
                neighbours.append(down)
        if cell.x > 0:
            east = self.maze_grid[cell.y][cell.x+1]
            if not east.visited and not self._has_wall_between(cell, east):
                neighbours.append(east)
        if cell.x < self.maze.width - 1:
            west = self.maze_grid[cell.y][cell.x-1]
            if not west.visited and not self._has_wall_between(cell, west):
                neighbours.append(west)
        return neighbours

    NORTH = 1  # 0001
    EAST = 2   # 0010
    SOUTH = 4  # 0100
    WEST = 8   # 1000
    ALL = 15   # 1111

    def _has_wall_between(self, cell_a: Cell, cell_b: Cell) -> bool:
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
        
        raise ValueError("Cells are not neighbours")



    def remove_walls(self, cell_a: Cell, cell_b: Cell) -> None:
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
        self._generate_maze_dfs()

        if self.perfect is False:
            self.create_multiple_paths()

        return self.maze.grid

    def _generate_maze_dfs(self) -> None:
        start = self.entry
        stack = []
        stack.append(start)
        start.visited = True

        while len(stack) > 0:
            current = stack[-1]
            neighbours = self.get_unvisited_neighbours(current)
            if len(neighbours) > 0:
                next = random.choice(neighbours)
                self.remove_walls(current, next)
                next.visited = True
                stack.append(next)
            else:
                stack.pop()

    def _create_multiple_paths(self) -> None:
        for _ in range(15):
            y: int = random.randint(0, self.height - 1)
            x: int = random.randint(0, self.width - 1)
            cell = self.maze.grid[y][x]
            neighbours = self.get_all_neighbours(cell)
            if not neighbours:
                continue
            nb = random.choice(neighbours)
            if self._has_wall_between(cell, nb):
                self.remove_walls(cell, nb)


    def solve_maze_bfs(self):
        queue = []
        self.entry.visited = True
        queue.append(self.entry)
        parents = {}

        while len(queue) > 0:
            current = queue.pop(0)
            if current == self.exit:
                return self.reconstruct_path(parents)
            neighbours = self.get_reachable_neighbours(current)
            for n in neighbours:
                if not n.visited:
                    n.visited = True
                    parents[n] = current
                    queue.append(n)
        return []
    
    def reconstruct_path(self, parents: dict[Cell, Cell]):
        exit = self.exit
        path = [exit]
        current = exit
        while current in parents:
            path.append(current)
        path.reverse()
        return path




            

