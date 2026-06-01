from .cell import Cell


class Maze:
    def __init__(
            self,
            width: int,
            height: int,
            entry: dict[str, int],
            exit: dict[str, int],
            grid: list[list[Cell]]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = grid
