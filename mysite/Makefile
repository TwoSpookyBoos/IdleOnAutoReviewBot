.PHONY: test

# Define the root of the project
PROJ_ROOT := $(shell git rev-parse --show-toplevel)

# Define the command to run pytest
PYTEST_CMD := pytest

# Determine the operating system
ifeq ($(OS),Windows_NT)
	# If running on Windows
    VENV_DIR := $(shell powershell "(Get-ChildItem -Path \"$(PROJ_ROOT)\" -Recurse -Filter \"activate.ps1\" -File).DirectoryName")
	PY_PATH := $(VENV_DIR)/python.exe
else
	# If running on Unix-like systems
	VENV_DIR := $(shell dirname $(shell find "$(PROJ_ROOT)" -name "activate" | head -1))
	PY_PATH := $(VENV_DIR)/python
endif

test:
	$(PY_PATH) -m $(PYTEST_CMD)
