# Azure Data Factory v2 - Unit Testing Framework

## Development

### Prerequisites

* poetry == 1.6.1

### Pre-Commit Hooks

We use pre-commit hooks to ensure that the code is formatted correctly and that the code is linted before committing.

To install the pre-commit hooks, run the following command:

```bash
poetry run pre-commit install
```

To run the pre-commit hooks use the following command (append `--all-files` to run on all files)):

```bash
poetry run pre-commit run
```

### Run Linting

We use Ruff to lint our code as it provides similar rule sets to well-established linters into one
(e.g., black, flake8, isort, and pydocstyle).

To run linting, run the following command:

```bash
poetry run ruff .
```

### Updating lock file

When updating Poetry's lock file your local cache can become outdated.
You can clear your cache with `poetry cache clear PyPI --all`
