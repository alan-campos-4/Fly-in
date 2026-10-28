NAME = fly-in.py

PYTHON = uv

GREEN = "\033[0;32m"
RED   = "\033[0;31m"
END   = "\033[0m"

.PHONY: install run debug clean lint lint-strict build fclean

.DEFAULT: help

help:
	@echo "  make install ........ Install the project dependencies"
	@echo "  make run ............ Execute the main script"
	@echo "  make debug .......... Execute the main script in debug mode"
	@echo "  make clean .......... Delete the extra folders"
	@echo "  make lint ........... Examine the project with flake and mypy"
	@echo ""
	@echo "  make fclean ......... Delete the virtual environment folder"

install:
	@echo "Installing dependencies..."
	@if $(BIN)/pip install -r requirements.txt; then \
		echo $(GREEN)"Installation complete."$(END); \
	else \
		echo $(RED)"Installation failed."$(END); \
	fi

run:
	@uv run $(NAME)

debug:
	@uv run --with-requirements $(NAME) python -m pdb $(NAME)

lint:
	@-flake8 . --exclude .git,.mypy_cache,.venv,__pycache__
	@-mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	@-flake8 . --exclude .git,.mypy_cache,.venv,__pycache__
	@-mypy . --strict --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

clean:
	@-find . -type f -name "*.pyc" -delete
	@-find . -path '*/__pycache__*' -delete
	@-find . -path '*/.mypy_cache*' -delete
	@-rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/
	@echo $(RED)"Directory cleared."$(END)

build:
	@uv build
