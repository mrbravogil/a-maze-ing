""" Clase Celda """

class Cell:
    def __init__(self, x: int, y: int, visited: bool) -> None:
        self.x: int = x
        self.y: int = y
        self.visited: bool = false
        self.entrance: bool = false
        self.exit: bool = false
        self.walls: dict = {
            'right': True,
            'left': True,
            'top': True,
            'bottom': True
        }
