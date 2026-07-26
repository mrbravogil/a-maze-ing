class Cell:
    """Represents a single cell in the maze.

    Stores the cell coordinates, wall bitmask, and helper flags used to
    indicate whether the cell is static, visited, the entrance, or the exit.
    """
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        walls: int = 15,
        static: bool = False,
        visited: bool = False,
        entrance: bool = False,
        exit: bool = False,
    ) -> None:
        self.x = x
        self.y = y
        self.walls = walls
        self.static = static
        self.visited = visited
        self.entrance = entrance
        self.exit = exit
