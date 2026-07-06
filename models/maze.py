from .cell import Cell
from .maze_generator import MazeGenerator


class Maze:
    def __init__(
            self,
            width: int,
            height: int,
            entry: Cell,
            exit: Cell) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[Cell]] = []

    
    def generate(self, maze_gen: MazeGenerator) -> Maze:
        maze_gen.maze_init()
        maze_gen.carve_entrance_exit()
        maze_gen.maze.grid = maze_gen.dfs_generate()
        maze_gen.reset_visited()
        self.maze.grid = maze_gen.maze.grid
        return self.maze
    
    def solve(self, maze_gen: MazeGenerator, algorithm: bool):
        maze_gen.reset_visited()
        if algorithm == "bfs":
            maze_gen.solve_maze_bfs()
        elif algorithm == "dfs":
            maze_gen.solve_maze_dfs()
        else:
            raise Exception("Unknown algorithm")
        
