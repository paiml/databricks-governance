# Contributing to Production Governance and MLOps with Databricks

Thank you for your interest in contributing to this project!

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/databricks-governance.git
   cd databricks-governance
   ```

3. Install dependencies:
   ```bash
   uv sync --all-extras
   ```

## Development Workflow

### Code Style

We use `ruff` for linting and formatting Python files:

```bash
# Check code style
uv run ruff check examples/

# Format code
uv run ruff format examples/
```

### Adding Examples

When adding new examples:

1. Place files in the appropriate `examples/` subdirectory (one subdirectory per lesson topic)
2. SQL files should use clear comments explaining each statement's purpose
3. Python files should be runnable as Databricks notebooks (cell-by-cell)
4. Ensure new examples map to a specific lesson in `course_outline.md`
5. Update `examples/README.md` if adding a new category

### SQL Conventions

- Use uppercase for SQL keywords (`CREATE`, `GRANT`, `SELECT`)
- Use fully-qualified three-level namespaces (`catalog.schema.table`)
- Add comments before each logical block of statements

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Ensure linting passes: `make lint`
4. Update documentation as needed
5. Submit a pull request

## Code of Conduct

Please be respectful and constructive in all interactions.

## Questions?

Open an issue for any questions about contributing.
