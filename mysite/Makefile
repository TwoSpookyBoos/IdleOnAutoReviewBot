.PHONY: test

# Define the root of the project
PROJ_ROOT := $(shell git rev-parse --show-toplevel)

# Define the command to run pytest
PYTEST_CMD := python -m pytest

# Determine the operating system
# Define the command to set PYTHONPATH
ifeq ($(OS),Windows_NT)
	# If running on Windows
	VENV_DIR := $(shell Get-ChildItem "$(PROJ_ROOT)" -Filter "*[Aa]ctivate*.ps1" | Select-Object -First 1).DirectoryName
	SOURCE_CMD := $(VENV_DIR)/Activate.ps1
else
	# If running on Unix-like systems
	VENV_DIR := $(shell dirname $(shell find "$(PROJ_ROOT)" -name "[Aa]ctivate*" | head -1))
	SOURCE_CMD := source "$(VENV_DIR)/activate"
endif

# Define the test target
test:
	@echo "Activating virtual environment..."
	@$(SOURCE_CMD)
	@echo "Running pytest..."
	@pytest

#test:
#	PYTHONPATH=$$(git rev-parse --show-toplevel)/mysite && cd "$$PYTHONPATH" && PYTHONPATH="$$PYTHONPATH" pytest
