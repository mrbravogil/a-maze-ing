class Cell:
    """ Cell Class """
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
