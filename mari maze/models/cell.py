class Cell:
    """ Cell Class """
    def __init__(
            self,
            walls: int = 15,
            static: bool = False,
            visited: bool = False) -> None:
        self.walls = walls
        self.static = static
        self.visited = False
        self.entrance: bool = False
        self.exit: bool = False
