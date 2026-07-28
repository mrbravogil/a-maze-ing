from setuptools import setup, find_packages

setup(
    name='a_maze_ing',
    version='0.1',
    description='A-Maze-ing is a Python project that generates random mazes.',
    author='mabravo-, aruiznav',
    packages=find_packages(),
    py_modules=["a_maze_ing", "config_parser", "maze_analyzer"],
    include_package_data=True,
    python_requires=">=3.10",
)
