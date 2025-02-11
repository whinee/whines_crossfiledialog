# Settings
set windows-shell := ['pwsh.exe', '-CommandWithArgs']
set positional-arguments

# Constants

# Choose recipes
default:
    @ just -lu; printf '%s ' press Enter to continue; read; just --choose

[private]
nio:
    @ python -m no_implicit_optional crossfiledialog; exit 0

[private]
ruff:
    @ python -m ruff check crossfiledialog --fix; exit 0

# Set up development environment
[unix]
bootstrap:
    #!/usr/bin/env bash
    python3.12 -m venv --system-site-packages .venv
    source .venv/bin/activate
    rm -rf poetry.lock
    poetry install --no-root --with dev

# Set up development environment
[windows]
bootstrap:
    python3.12 -m venv --system-site-packages .venv
    . .\.venv\Scripts\Activate.ps1
    Remove-Item -Force -Recurse poetry.lock
    poetry install --no-root --with dev

# Lint codebase
lint:
    @ just nio
    @ python -m black -q crossfiledialog
    @ just ruff
