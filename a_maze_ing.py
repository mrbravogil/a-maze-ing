"""A-Maze-ing: Interactive maze generator and visualizer.

This module provides the main entry point for the A-Maze-ing project.
It loads a configuration file, generates a maze, writes it to an output
file, and provides an interactive ASCII terminal interface.

Usage:
    python3 a_maze_ing.py <config_file>
"""

import os
import random
import sys

from config_parser import ConfigParser, ConfigError, Config
from models.maze_generator import MazeGenerator
from models.cell import Cell


class MazeApp:
    """Main application class for the A-Maze-ing maze generator.

    Handles configuration loading, maze generation, output writing,
    and interactive ASCII terminal display.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    ANSI_RESET = "\033[0m"
    ANSI_GREEN = "\033[92m"
    ANSI_RED = "\033[91m"
    ANSI_CYAN = "\033[96m"
    ANSI_YELLOW = "\033[93m"

    WALL_COLORS = [
        ("white", "\033[97m"),
        ("red", "\033[91m"),
        ("green", "\033[92m"),
        ("yellow", "\033[93m"),
        ("blue", "\033[94m"),
        ("magenta", "\033[95m"),
        ("cyan", "\033[96m"),
    ]

    def __init__(self) -> None:
        """Initialize the MazeApp with default state."""
        self.config: Config | None = None
        self.generator: MazeGenerator | None = None
        self.solution: list[Cell] = []
        self.show_path = False
        self.wall_color_index = 0
        self.wall_color = self.WALL_COLORS[0][1]
        self.use_colors = True

    def _parse_args(self) -> str:
        """Parse command-line arguments.

        Returns the path to the configuration file.

        Exits if the number of arguments is not exactly 2.
        """
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py "
                  "<config_file>", file=sys.stderr)
            sys.exit(1)
        return sys.argv[1]

    def _load_config(self, filepath: str) -> Config:
        """Load and parse the configuration file.

        Returns a Config object with parsed configuration values.

        Exits if the configuration is invalid.
        """
        try:
            parser = ConfigParser(filepath)
            return parser.parse()
        except ConfigError as exc:
            print(f"Configuration Error: {exc}", file=sys.stderr)
            sys.exit(1)

    def _generate_maze(self) -> None:
        """Generate the maze using the loaded configuration.

        Creates a MazeGenerator instance, initializes the maze,
        carves entrance and exit, and generates the maze structure.
        For imperfect mazes, additional paths are created to form loops.

        Raises aValueError: If maze generation parameters are invalid.
        """
        self.generator = MazeGenerator(
            width=self.config.width,
            height=self.config.height,
            entry_x=self.config.entry[0],
            entry_y=self.config.entry[1],
            exit_x=self.config.exit[0],
            exit_y=self.config.exit[1],
            perfect=self.config.perfect,
            seed=self.config.seed,
        )
        self.generator.maze_init()
        self.generator.carve_entrance_exit()
        self.generator.dfs_generate()

        if not self.config.perfect:
            self.generator._create_multiple_paths()

        self.generator.reset_visited()
        self.solution = self.generator.solve_maze_bfs(
            self.generator.entry,
            self.generator.exit,)

    def _cell_to_hex(self, cell: Cell) -> str:
        """Convert a cell's wall bitmask to a hexadecimal character.

        Returns a single hexadecimal character representing the cell's walls.
        """
        return format(cell.walls, "x")

    def _path_to_directions(self, path: list[Cell]) -> str:
        """Convert a list of cells to a direction string.

        Returns a string of directions (N, E, S, W) representing the path.
        Returns an empty string if the path has fewer than 2 cells.
        """
        if len(path) < 2:
            return ""
        directions = []
        for i in range(len(path) - 1):
            current = path[i]
            next_cell = path[i + 1]
            dx = next_cell.x - current.x
            dy = next_cell.y - current.y
            if dx == 1:
                directions.append("E")
            elif dx == -1:
                directions.append("W")
            elif dy == 1:
                directions.append("S")
            elif dy == -1:
                directions.append("N")
        return "".join(directions)

    def _write_output(self) -> None:
        """Write the generated maze to the output file. """
        try:
            with open(self.config.output_file, "w", encoding="utf-8") as f:
                for row in self.generator.maze.grid:
                    line = "".join(self._cell_to_hex(cell) for cell in row)
                    f.write(line + "\n")
                f.write("\n")
                f.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
                f.write(f"{self.config.exit[0]},{self.config.exit[1]}\n")
                path_str = self._path_to_directions(self.solution)
                f.write(path_str + "\n")
            print(f"Maze written to: {self.config.output_file}")
        except OSError as exc:
            print(f"Error writing output file: {exc}", file=sys.stderr)
            sys.exit(1)

    def _render_ascii(self) -> str:
        """Render the maze as an ASCII string with ANSI colors.

        Returns a multi-line string representing the maze with walls,
        entrance, exit, solution path, and the "42" pattern.
        """
        grid = self.generator.maze.grid
        h = self.config.height
        w = self.config.width
        solution_set = {
            cell for cell in self.solution} if self.solution else set()

        lines = []
        top = ""
        for x in range(w):
            cell = grid[0][x]
            if cell.walls & self.NORTH:
                top += "+---"
            else:
                top += "+   "
        top += "+"
        lines.append(self.wall_color + top + self.ANSI_RESET)

        for y in range(h):
            content = ""
            for x in range(w):
                cell = grid[y][x]
                if cell.walls & self.WEST:
                    content += self.wall_color + "|" + self.ANSI_RESET
                else:
                    content += " "

                if cell.static:
                    content += (self.ANSI_YELLOW + "███"
                                + self.ANSI_RESET + self.wall_color)
                elif cell.entrance:
                    content += (self.ANSI_GREEN + " E "
                                + self.ANSI_RESET + self.wall_color)
                elif cell.exit:
                    content += (self.ANSI_RED + " X "
                                + self.ANSI_RESET + self.wall_color)
                elif self.show_path and cell in solution_set:
                    content += (self.ANSI_CYAN + " * "
                                + self.ANSI_RESET + self.wall_color)

                else:
                    content += "   "

            last = grid[y][-1]
            if last.walls & self.EAST:
                content += self.wall_color + "|" + self.ANSI_RESET
            else:
                content += " "

            lines.append(content + self.ANSI_RESET)

            horiz = ""
            for x in range(w):
                cell = grid[y][x]
                if cell.walls & self.SOUTH:
                    horiz += self.wall_color + "+---" + self.ANSI_RESET
                else:
                    horiz += self.wall_color + "+   " + self.ANSI_RESET
            horiz += self.wall_color + "+" + self.ANSI_RESET
            lines.append(self.wall_color + horiz + self.ANSI_RESET)

        return "\n".join(lines)

    def _display_menu(self) -> None:
        """Display the interactive menu options."""
        print()
        print("=" * 40)
        print("         A-Maze-ing")
        print("=" * 40)
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Change the wall colours")
        print("4. Toggle colours on/off")
        print("5. Quit")
        print("-" * 40)

    def _run_interactive(self) -> None:
        """Run the interactive terminal loop.

        Continuously displays the maze and menu, processing user input
        to regenerate, toggle path display, rotate colors, or quit.
        """
        while True:
            try:
                os.system("cls" if os.name == "nt" else "clear")
                print(self._render_ascii())
                self._display_menu()

                try:
                    choice = input("Choice? (1-5): ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye!")
                    break

                if choice == "1":
                    if self.config.seed is None:
                        self.config.seed = random.randint(1, 1000000)
                    else:
                        self.config.seed += 1
                    self._generate_maze()
                    self._write_output()
                    print("Maze regenerated!")
                    input("Press Enter to continue...")

                elif choice == "2":
                    self.show_path = not self.show_path
                    status = "shown" if self.show_path else "hidden"
                    print(f"Path {status}.")
                    input("Press Enter to continue...")

                elif choice == "3":
                    self.wall_color_index = (
                        self.wall_color_index + 1) % len(self.WALL_COLORS)

                    self.wall_color = self.WALL_COLORS[
                        self.wall_color_index][1]

                    print(f"Wall colour: "
                          f"{self.WALL_COLORS[self.wall_color_index][0]}")

                    input("Press Enter to continue...")

                elif choice == "4":
                    self.use_colors = not self.use_colors
                    status = "enabled" if self.use_colors else "disabled"
                    print(f"Colours {status}.")
                    input("Press Enter to continue...")

                elif choice == "5":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1-5.")
                    input("Press Enter to continue...")

            except (EOFError, KeyboardInterrupt):
                break
            except Exception as exc:
                print(f"\nError: {exc}", file=sys.stderr)
                input("Press Enter to continue...")

    def run(self) -> None:
        """Run the main application flow.

        Parses arguments, loads configuration, generates the maze,
        writes the output file, and starts the interactive loop.
        """
        config_path = self._parse_args()
        self.config = self._load_config(config_path)

        print("Configuration loaded:")
        print(f"  Width: {self.config.width}")
        print(f"  Height: {self.config.height}")
        print(f"  Entry: {self.config.entry}")
        print(f"  Exit: {self.config.exit}")
        print(f"  Perfect: {self.config.perfect}")
        print(f"  Seed: {self.config.seed}")
        print(f"  Output: {self.config.output_file}")
        print()

        try:
            self._generate_maze()
        except ValueError as exc:
            print(f"Maze generation error: {exc}", file=sys.stderr)
            sys.exit(1)

        print(f"Maze generated! Path length: {len(self.solution)} steps")
        self._write_output()
        self._run_interactive()


def main() -> None:
    """Main entry point for the A-Maze-ing application."""
    app = MazeApp()
    app.run()


if __name__ == "__main__":
    main()
