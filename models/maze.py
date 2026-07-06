from .cell import Cell


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
