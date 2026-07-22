"""Configuration parser for the A-Maze-ing project.

This module provides the ConfigParser class to read and validate
maze generation configuration files in KEY=VALUE format.

Example configuration file::

    WIDTH=20
    HEIGHT=15
    ENTRY=0,0
    EXIT=19,14
    OUTPUT_FILE=maze.txt
    PERFECT=True
    SEED=42
"""

import os
import sys

from dataclasses import dataclass
from typing import Any


class ConfigError(Exception):
    """Raised when a configuration file contains invalid data."""
    pass


@dataclass
class Config:
    """Holds parsed maze generation configuration values.

    Attributes:
        width: Number of cells in the horizontal direction.
        height: Number of cells in the vertical direction.
        entry: Tuple of (x, y) coordinates for the maze entrance.
        exit: Tuple of (x, y) coordinates for the maze exit.
        output_file: Path to the file where the maze will be written.
        perfect: Whether the maze must have exactly one path (True)
                 or be a playable board with loops (False).
        seed: Optional integer seed for reproducible maze generation.
        extra: Dictionary of additional configuration keys, if any.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    extra: dict[str, Any] | None = None


class ConfigParser:
    """Parser for A-Maze-ing configuration files.

    Reads a plain text file containing KEY=VALUE pairs, validates
    required fields, and returns a Config dataclass instance.
    """

    REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT",
                     "OUTPUT_FILE", "PERFECT"}

    def __init__(self, filepath: str) -> None:
        """Initialize the parser with a configuration file path.

        Raises ConfigError: If filepath is empty or not a string.
        """
        if not filepath or not isinstance(filepath, str):
            raise ConfigError(
                "Configuration file path must be a non-empty string.")
        self.filepath = filepath

    def _read_file(self) -> list[str]:
        """Read and preprocess the configuration file.

        Removes empty lines and lines starting with '#'.

        Returns a List of non-empty, non-comment configuration lines.

        Raises ConfigError: If the file does not exist, is not readable,
        or contains only comments/empty lines.
        """
        if not os.path.exists(self.filepath):
            raise ConfigError(
                f"Configuration file not found: '{self.filepath}'")
        if not os.path.isfile(self.filepath):
            raise ConfigError(
                f"Configuration path is not a file: '{self.filepath}'")

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except OSError as exc:
            raise ConfigError(
                f"Cannot read configuration file "
                f"'{self.filepath}': {exc}") from exc

        processed_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                processed_lines.append(stripped)

        if not processed_lines:
            raise ConfigError(
                f"Configuration file '{self.filepath}' "
                f"is empty or contains only comments.")

        return processed_lines

    def _parse_lines(self, lines: list[str]) -> dict[str, str]:
        """Parse configuration lines into a key-value dictionary.

        Returns a Dictionary mapping uppercase keys to their string values.

        Raises ConfigError: If a line has invalid format, empty key/value,
        or duplicate key.
        """
        config = {}

        for line in lines:
            if "#" in line:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue

            if "=" not in line:
                raise ConfigError(
                    f"Invalid line in configuration file: '{line}'. "
                    f"Expected format: KEY=VALUE")

            key_part, value_part = line.split("=", 1)
            key = key_part.strip().upper()
            value = value_part.strip()

            if not key:
                raise ConfigError(f"Empty key in configuration line: '{line}'")
            if not value:
                raise ConfigError(
                    f"Empty value for key '{key}' in configuration file.")
            if key in config:
                raise ConfigError(
                    f"Duplicate key '{key}' in configuration file.")

            config[key] = value

        return config

    def _validate_required_keys(self, config: dict[str, str]) -> None:
        """Check that all required configuration keys are present.

        Raises ConfigError: If any required key is missing.
        """
        missing = self.REQUIRED_KEYS - config.keys()
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ConfigError(
                f"Missing required configuration keys: {missing_list}")

    def _parse_width(self, value: str) -> int:
        """Parse and validate the WIDTH value.

        Returns a positive integer width.

        Raises ConfigError: If value is not a positive integer.
        """
        try:
            width = int(value)
        except ValueError as exc:
            raise ConfigError(
                f"WIDTH must be an integer, got: '{value}'") from exc
        if width <= 0:
            raise ConfigError(
                f"WIDTH must be a positive integer, got: {width}")
        return width

    def _parse_height(self, value: str) -> int:
        """Parse and validate the HEIGHT value.

        Returns a positive integer height.

        Raises ConfigError: If value is not a positive integer.
        """
        try:
            height = int(value)
        except ValueError as exc:
            raise ConfigError(
                f"HEIGHT must be an integer, got: '{value}'") from exc
        if height <= 0:
            raise ConfigError(
                f"HEIGHT must be a positive integer, got: {height}")
        return height

    def _parse_coordinates(self, value: str, key_name: str) -> tuple[int, int]:
        """Parse a comma-separated coordinate pair.

        Returns a Tuple of (x, y) non-negative integer coordinates.

        Raises ConfigError: If format is invalid or coordinates are negative.
        """
        parts = value.split(",")
        if len(parts) != 2:
            raise ConfigError(
                f"{key_name} must be in format 'x,y', got: '{value}'")

        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError as exc:
            raise ConfigError(
                f"{key_name} coordinates must be "
                f"integers, got: '{value}'") from exc

        if x < 0 or y < 0:
            raise ConfigError(
                f"{key_name} coordinates must be "
                f"non-negative, got: ({x}, {y})")

        return (x, y)

    def _parse_perfect(self, value: str) -> bool:
        """Parse the PERFECT boolean value.

        Returns True for "true", "1", "yes", "on"; False otherwise.

        Raises ConfigError: If value is not a recognized boolean.
        """
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes", "on"):
            return True
        if normalized in ("false", "0", "no", "off"):
            return False
        raise ConfigError(
            f"PERFECT must be a boolean (True/False), got: '{value}'")

    def _parse_seed(self, value: str) -> int:
        """Parse the SEED integer value.

        Returns a Integer seed value.

        Raises ConfigError: If value is not an integer.
        """
        try:
            return int(value)
        except ValueError as exc:
            raise ConfigError(
                f"SEED must be an integer, got: '{value}'") from exc

    def _validate_entry_exit_bounds(
        self,
        entry: tuple[int, int],
        exit_coords: tuple[int, int],
        width: int,
        height: int,
    ) -> None:
        """Validate that entry and exit coordinates are within maze bounds.

        Raises ConfigError: If coordinates are out of bounds or identical.
        """
        ex, ey = entry
        xx, xy = exit_coords

        if not (0 <= ex < width and 0 <= ey < height):
            raise ConfigError(
                f"ENTRY coordinates ({ex}, {ey}) are out of bounds. "
                f"Valid range: (0-{width - 1}, 0-{height - 1})")
        if not (0 <= xx < width and 0 <= xy < height):
            raise ConfigError(
                f"EXIT coordinates ({xx}, {xy}) are out of bounds. "
                f"Valid range: (0-{width - 1}, 0-{height - 1})")
        if ex == xx and ey == xy:
            raise ConfigError("ENTRY and EXIT coordinates must be different.")

    def _validate_output_path(self, output_file: str) -> None:
        """Validate that the output file directory exists and is writable.

        Raises ConfigError: If the parent directory does not exist.
        """
        parent_dir = os.path.dirname(os.path.abspath(output_file))
        if parent_dir and not os.path.isdir(parent_dir):
            raise ConfigError(
                f"Output directory does not exist: '{parent_dir}'")

    def _warn_maze_size(self, width: int, height: int) -> None:
        """Print a warning if the maze may be too small for the '42' pattern.
        """
        if width < 9 or height < 6:
            print(
                f"Warning: Maze size ({width}x{height}) may be too small "
                f"for the '42' pattern. The pattern will be omitted.",
                file=sys.stderr,
            )

    def parse(self) -> Config:
        """Parse the configuration file and return a Config instance.

        Reads the file, validates required keys, parses each field,
        and returns a fully validated Config object.

        Returns the config instance with all parsed and validated values.

        Raises a ConfigError: If any validation fails.
        """
        lines = self._read_file()
        raw_config = self._parse_lines(lines)
        self._validate_required_keys(raw_config)

        width = self._parse_width(raw_config["WIDTH"])
        height = self._parse_height(raw_config["HEIGHT"])
        entry = self._parse_coordinates(raw_config["ENTRY"], "ENTRY")
        exit_coords = self._parse_coordinates(raw_config["EXIT"], "EXIT")
        output_file = raw_config["OUTPUT_FILE"]
        perfect = self._parse_perfect(raw_config["PERFECT"])

        self._validate_entry_exit_bounds(entry, exit_coords, width, height)
        self._validate_output_path(output_file)
        self._warn_maze_size(width, height)

        seed = None
        extra = {}

        for key, value in raw_config.items():
            if key in self.REQUIRED_KEYS:
                continue
            if key == "SEED":
                seed = self._parse_seed(value)
            else:
                extra[key] = value

        return Config(
            width=width,
            height=height,
            entry=entry,
            exit=exit_coords,
            output_file=output_file,
            perfect=perfect,
            seed=seed,
            extra=extra if extra else None,
        )


def parse_config(filepath: str) -> Config:
    """Convenience function to parse a configuration file.

    Returns parsed and validated Config instance.
    """
    parser = ConfigParser(filepath)
    return parser.parse()
