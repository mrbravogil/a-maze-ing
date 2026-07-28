PACKAGE  = a_maze_ing
NAME     = a_maze_ing.py
CONFIG   = config.txt
PYTHON   = python3
PIP      = pip

all: run

install:
	$(PYTHON) -m $(PIP) install flake8 mypy

install-user:
	$(PYTHON) -m $(PIP) install --user flake8 mypy

run:
	$(PYTHON) $(NAME) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(NAME)

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

package:
	$(PYTHON) setup.py sdist bdist_wheel

clean:
	rm -rf dist/ build/ *.egg-info
	rm -rf *.tar.gz *.whl
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} \;

.PHONY: all install run debug lint clean