# Contributing

Thanks for your interest in contributing to finwise-python!

## Development Setup

### Option 1: Using Nix (Recommended)

If you have [Nix](https://nixos.org/) installed with flakes enabled:

```bash
git clone https://github.com/rameezk/finwise-python.git
cd finwise-python

# Enter development shell
nix develop

# Install package in editable mode
pip install -e .
```

Available dev shells:
- `nix develop` - Default (Python 3.11)
- `nix develop .#python312` - Python 3.12
- `nix develop .#python313` - Python 3.13
- `nix develop .#docs` - Documentation environment

### Option 2: Using virtualenv

1. Clone the repository:
   ```bash
   git clone https://github.com/rameezk/finwise-python.git
   cd finwise-python
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov --cov-report=term-missing
```

## Code Quality

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting, and [mypy](https://mypy-lang.org/) for type checking.

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy src/
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Ensure tests pass and code quality checks succeed
5. Commit your changes using [conventional commits](https://www.conventionalcommits.org/)
6. Push to your fork and open a pull request

## Commit Messages

This project uses [semantic-release](https://python-semantic-release.readthedocs.io/) for automated versioning. Please use conventional commit messages:

- `feat:` - New features (triggers minor version bump)
- `fix:` - Bug fixes (triggers patch version bump)
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks
- `test:` - Test changes
- `refactor:` - Code refactoring

Example:
```
feat: add support for bulk transactions
fix: handle pagination edge case
docs: update installation instructions
```

## Questions?

Open an issue if you have questions or run into problems.
