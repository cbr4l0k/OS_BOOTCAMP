# Python Project Conventions

## Directory Structure

```
project-name/
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py
│       └── api/ (for API projects)
├── tests/
│   └── __init__.py
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── Dockerfile (if needed)
└── docker-compose.yml (if needed)
```

## pyproject.toml Structure

Use modern Python packaging with pyproject.toml (PEP 621). Include:
- Project metadata (name, version, description, authors)
- Dependencies in `[project.dependencies]`
- Dev dependencies in `[project.optional-dependencies]`
- Tool configurations (black, ruff, mypy, pytest)

## Pre-commit Hooks

Standard Python pre-commit hooks:
- `ruff` for linting and import sorting
- `black` for formatting
- `mypy` for type checking (optional, but recommended)

## Linting & Formatting

- **Formatter**: Black (opinionated, no config needed)
- **Linter**: Ruff (fast, replaces flake8, isort, etc.)
- **Type checker**: mypy (optional but increasingly standard)

## Docker Considerations

For APIs:
- Multi-stage build (builder + runtime)
- Use official Python slim images
- Install dependencies first (layer caching)
- Non-root user for security
- Health check endpoint

For scripts/tools:
- Single stage usually sufficient
- Alpine base if size matters
