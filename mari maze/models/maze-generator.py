from . import Maze, Cell


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
        self.maze = maze_class.grid
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

    def get_neighbours(self, cell: Cell, maze: Maze) -> list[Cell]:
        neighbours: list[Cell] = []
        if cell.y > 0:
            neighbours.append(Cell(cell.y+1, cell.x))
        if cell.y < maze.height - 1:
            neighbours.append(Cell(cell.y-1, cell.x))
        if cell.x > 0:
            neighbours.append(Cell(cell.y, cell.x+1))
        if cell.x < maze.width - 1:
            neighbours.append(Cell(cell.y, cell.x-1))
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
