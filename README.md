# Python Template

## Features

- Poetry
- pre-commit
    - flake8
    - black
    - isort
    - autoflake
    - mypy
    - prettier
- Python3.9

## Usage

```bash
poetry install
poetry run pre-commit install --install-hooks -c .pre-commit-config.yaml
```

## Update pre-commit hooks

```bash
poetry run pre-commit autoupdate
```

