################################################################################
# Windows-only Makefile (runs under cmd.exe or PowerShell)
# Uses the venv's python -m to avoid .exe + path issues.
################################################################################

.PHONY: all help venv run format format-check lint mypy test dist clean

# Force GNU Make to use cmd.exe on Windows (harmless if already using cmd)
SHELL := cmd
.SHELLFLAGS := /C

PY ?= python
VENV_DIR := venv
VENV_PY := $(VENV_DIR)\Scripts\python.exe

# Module runners (robust: always go through the venv's python)
PIP    := "$(VENV_PY)" -m pip
FLASK  := "$(VENV_PY)" -m flask
PYTEST := "$(VENV_PY)" -m pytest
BLACK  := "$(VENV_PY)" -m black
ISORT  := "$(VENV_PY)" -m isort
FLAKE8 := "$(VENV_PY)" -m flake8
MYPY   := "$(VENV_PY)" -m mypy

all: run

help:
	@echo Available targets:
	@echo   make venv          - create virtual environment + install deps
	@echo   make run           - run Flask dev server (debug reload)
	@echo   make format        - apply black + isort formatting
	@echo   make format-check  - check formatting without modifying files
	@echo   make lint          - run flake8
	@echo   make mypy          - run mypy type checking
	@echo   make test          - run pytest
	@echo   make dist          - build wheel (after checks/tests)
	@echo   make clean         - remove venv and build artifacts

$(VENV_DIR):
	$(PY) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .
	$(PIP) install -e ".[dev]"

# Alias so both `make venv` and directory existence work
venv: $(VENV_DIR)

run: venv
	$(FLASK) --app synced_ereader_api --debug run

format: venv
	$(BLACK) .
	$(ISORT) .

format-check: venv
	$(BLACK) --check .
	$(ISORT) --check .

lint: venv
	$(FLAKE8) .

mypy: venv
	$(MYPY)

test: venv
	$(PYTEST)

dist: venv format-check lint mypy test
	$(PIP) wheel --wheel-dir dist --no-deps .

clean:
	@echo Removing virtual environment and build artifacts...
	$(PY) -c "import shutil,glob,os; [shutil.rmtree(p, ignore_errors=True) for p in ['venv','build','dist','.pytest_cache','.mypy_cache']]; [shutil.rmtree(d, ignore_errors=True) for d in glob.glob('*.egg-info')]; print('Done.')"
