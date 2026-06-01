from .maze import Maze
from .cell import Cell


class MazeGenerator:
    """ Maze Generator Class """
    def __init__(
        self,
        config_file: str,
        animation: bool
     ) -> None:
        maze_class = Maze()
        self.width = maze_class.width
        self.heigth = maze_class.heigth
        self.animation = animation
        self.maze = maze_class.grid
        self.seed = seed
        self.perfect = perfect
        self.entry = maze_class.entry
        self.exit = maze_class.exit
        self.solutions: list[list[str]] = []
        self.maze_init()

    def maze_init(self) -> None:
        for y in range(self.heigth):
            row: list = []
            for x in range(self.width):
                cell: Cell = Cell(15, False, False)
                row.append(cell)
            self.maze.append(row)

        if self.width < 7 or self.heigth < 5:
            print("'Error: Maze size is too small for '42' pattern.")
            exit(0)

        offset_x: int = (self.width - 7) // 2
        offset_y: int = (self.heigth - 5) // 2

        pattern_42: list[str] = [
            "#..#..####",
            "#..#.....#.",
            "####....#..",
            "...#...#...",
            "...#..#####",
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
