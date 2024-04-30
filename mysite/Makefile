.PHONY: test

# Define the root of the project
PROJ_ROOT := $(shell git rev-parse --show-toplevel)

# Define the command to run pytest
PYTEST_CMD := pytest

# Determine the operating system
ifeq ($(OS),Windows_NT)
	# If running on Windows
	VENV_DIR := $(shell Get-ChildItem "$(PROJ_ROOT)" -Filter "*[Aa]ctivate*.ps1" | Select-Object -First 1).DirectoryName
	SOURCE_CMD := $(VENV_DIR)/*ctivate.ps1
else
	# If running on Unix-like systems
	VENV_DIR := $(shell dirname $(shell find "$(PROJ_ROOT)" -name "[Aa]ctivate*" | head -1))
	SOURCE_CMD := source $(VENV_DIR)/*ctivate
endif

test:
	$(SOURCE_CMD) && $(PYTEST_CMD)
