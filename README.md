*This project has been created as part of the 42 curriculum by mabravo-, aruiznav*

# A-Maze-ing
A-Maze-ing is a Python project that generates random mazes from a configuration file. Depending on the selected mode, the program can generate either:

- **A perfect maze**, where there is exactly one unique path between the entrance and the exit.
- **A playable maze** designed for a Pac-Man-like game, containing loops and multiple alternative routes while remaining fully connected.

The project reads a configuration file, generates the maze using a randomized algorithm, computes the shortest solution, saves the maze using a hexadecimal wall encoding, and provides a visual representation in the terminal.

The maze generator has also been designed as a **reusable Python package** that can be imported into future projects.


## Features

- Random maze generation
- Reproducible mazes using a seed
- Perfect and non-perfect generation modes
- Automatic shortest path calculation
- ASCII terminal visualization
- Show / Hide shortest path
- Regenerate mazes without restarting the application
- Configurable wall colors
- Export to hexadecimal format
- Reusable Python package


## Instructions

### Requirements

- Python 3.10+
- `flake8`
- `mypy`

### Installation

```bash
make install
```

### Run the project

```bash
make run
```

Or directly:

```bash
python3 a_maze_ing.py config.txt
```

### Debug mode

```bash
make debug
```

### Static analysis

```bash
make lint
```

### Strict analysis

```bash
make lint-strict
```

### Clean cache files

```bash
make clean
```


## Configuration File

The program receives a configuration file containing one `KEY=VALUE` pair per line.

### Example

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

### Configuration Keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width (number of cells) | `WIDTH=20` |
| `HEIGHT` | Maze height (number of cells) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `(x,y)` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `(x,y)` | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Generates a perfect maze when `True` | `PERFECT=True` |
| `SEED` | *(Optional)* Random seed for reproducibility | `SEED=42` |

> **Note:** Lines beginning with `#` are ignored.

### Full Example

```text
# Example configuration

WIDTH=30
HEIGHT=20
ENTRY=0,0
EXIT=29,19
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=12345
```

## Maze Generation Algorithm

The maze is generated using the **Recursive Backtracker algorithm** (Depth-First Search).

### Algorithm Overview

1. Start from the entry cell.
2. Mark it as visited.
3. Randomly select one unvisited neighbour.
4. Remove the wall between both cells.
5. Continue recursively until every cell has been visited.
6. Backtrack whenever a dead end is reached.

When `PERFECT=True`, this algorithm naturally generates a perfect maze because every cell belongs to a spanning tree.

When `PERFECT=False`, additional walls are removed after generation in order to:

- Create loops.
- Reduce dead ends.
- Provide multiple independent routes.
- Preserve full connectivity.

### Why This Algorithm?

The Recursive Backtracker was chosen because:

- It is simple to understand and implement.
- It guarantees a perfect maze.
- It is fast — `O(width × height)`.
- It produces long and interesting corridors.
- It can easily be adapted to generate non-perfect mazes by removing additional walls.


## Output File Format

The maze is stored using hexadecimal values. Each hexadecimal digit represents the walls surrounding one cell.

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A value of `1` means the wall exists.

### Example

```text
A
```

Binary: `1010`

| Direction | State |
|-----------|-------|
| North | Open |
| East | Closed |
| South | Open |
| West | Closed |

After the maze grid, the output file contains three extra lines:

1. Entry coordinates `(x,y)`
2. Exit coordinates `(x,y)`
3. Shortest path using `N`, `E`, `S`, `W`


## Visual Representation

The maze is displayed directly in the terminal using ASCII characters.

### Available Interactions

| Option | Action |
|--------|--------|
| `1` | Generate a new maze |
| `2` | Show / Hide the shortest path |
| `3` | Change wall colors |
| `4` | Toggle colors on/off |
| `5` | Quit |

### Highlights

- Walls
- Entrance (`E`)
- Exit (`X`)
- Shortest path (`*`)


## Reusable Module

The maze generator is implemented as a standalone class: `MazeGenerator`.

### Quick Start

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry_x=0,
    entry_y=0,
    exit_x=19,
    exit_y=14,
    seed=42,
    perfect=True
)

maze.maze_init()
maze.carve_entrance_exit()
maze.dfs_generate()

solution = maze.solve_maze_bfs(maze.entry, maze.exit)
grid = maze.maze.grid
```

### Provided Features

- Maze generation (`dfs_generate`)
- Maze solving (`solve_maze_bfs`, `solve_maze_dfs`)
- Access to individual cells
- Access to wall bitmasks
- Access to the shortest path

The package can be built using standard Python packaging tools and installed with:

```bash
pip install mazegen-*.whl
```


## Project Structure

```text
.
├── a_maze_ing.py          # Main entry point
├── config.txt             # Default configuration
├── Makefile               # Automation rules
├── README.md              # This file
├── LICENSE.md             # MIT License
├── requirements.txt       # Python dependencies
├── models/
│   ├── __init__.py
│   ├── cell.py
│   ├── maze.py
│   └── maze_generator.py
└── maze.txt
```

## Team Organization

### Roles

| Member | Responsibilities |
|--------|------------------|
| `mabravo-` | Project architecture, maze generation, documentation |
| `aruiznav` | Visualization, configuration parser, tests, documentation |

### Planning

**Initial planning:**

1. Configuration parser
2. Maze generator
3. Solver
4. Export
5. Visualization
6. Documentation

During development we adjusted the schedule to first finish the generator before implementing visualization. This allowed easier testing and debugging.

### Retrospective

**What worked well:**

- Good task separation.
- Modular code.
- Continuous testing.
- Frequent Git commits.

**What could be improved:**

- Better early planning for visualization.

### Tools Used

- Python 3
- Git / GitHub
- VS Code
- `flake8`
- `mypy`



## Resources

### Documentation

- [Python Documentation](https://docs.python.org/)
- [PEP 8](https://peps.python.org/pep-0008/)
- [PEP 257](https://peps.python.org/pep-0257/)
- [typing documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

### Maze Algorithms

- [Recursive Backtracker](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search)
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory)
- [Spanning Trees](https://en.wikipedia.org/wiki/Spanning_tree)

### References

- https://docs.python.org/
- https://flake8.pycqa.org/
- https://mypy.readthedocs.io/
- https://en.wikipedia.org/wiki/Maze_generation_algorithm


## AI Usage

Artificial Intelligence was used as a development assistant for:

- Explaining maze generation algorithms.
- Finding errors

All generated content was reviewed, understood, tested, and adapted before being included in the final project.


## License

This project is distributed under the terms described in [LICENSE.md](LICENSE.md).

The reusable maze generator may be reused and redistributed according to that license.
