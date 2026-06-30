from . import Maze, Cell
import random


class MazeGenerator:
    """ Maze Generator Class """
    def __init__(
        self,
        config_file: str,
        animation: bool
     ) -> None:
        maze_class = Maze()
        self.width = maze_class.width
        self.height = maze_class.height
        self.animation = animation
        self.maze_grid = maze_class.grid
        self.seed = seed
        self.perfect = perfect
        self.entry = maze_class.entry
        self.exit = maze_class.exit
        self.solutions: list[list[str]] = []
        self.maze_init()

    def maze_init(self) -> None:
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                cell: Cell = Cell(x=x, y=y)
                row.append(cell)
            self.maze.append(row)
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
                self.maze[ty][tx].walls = 15
                self.maze[ty][tx].static = True
                self.maze[ty][tx].visited = True

    def get_neighbours(self, cell: Cell) -> list[Cell]:
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

    NORTH = 1  # 0001
    EAST = 2   # 0010
    SOUTH = 4  # 0100
    WEST = 8   # 1000
    ALL = 15   # 1111

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

    def generate_maze_dfs(self):
        start = self.entry
        stack = []
        stack.append(start)
        start.visited = True

        while len(stack) > 0:
            current = stack[-1]
            neighbours = self.get_neighbours(current)
            if len(neighbours) > 0:
                next = random.choice(neighbours)
                self.remove_walls(current, next)
                next.visited = True
                stack.append(next)
            else:
                stack.pop()


    def solve_maze_bfs(self):
        queue = []
        self.entry.visited = True
        queue.append(self.entry)
        parents = {}

        while len(queue) > 0:
            current = queue.pop(0)
            if current == self.exit:
                return self.reconstruct_path(parents)
            neighbours = self.get_neighbours(current)
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
