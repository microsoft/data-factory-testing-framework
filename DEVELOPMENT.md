# Azure Data Factory v2 - Unit Testing Framework

## Development

### Prerequisites

* poetry == 1.6.1

### Installing the project

Make sure to create a virtual environment and install the requirements by running:
`poetry install --with dev`

Build the .NET project:
`dotnet build`

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

### Run tests

We use pytest to test our code, coverage.py to generate coverage reports and [coverage gutters](https://marketplace.visualstudio.com/items?itemName=semasquare.vscode-coverage-gutters#:~:text=Features.%20Supports%20any%20language%20as%20long%20as%20you) VSCode extension to visualize code coverage in the editor.

To run all tests and generate coverage data run the following command:

```bash
poetry run coverage run --source=src -m pytest .
```

This will generate a .coverage file. To visualize code coverage, generate a coverage.xml file from the .coverage file by running:

```bash
poetry run coverage xml
```

Once the xml file is generated, you can view the coverage results in the editor by running the `Coverage Gutters: Watch` command.

To run tests and generate coverage.xml in a single command, run:

```bash
poetry run coverage run --source=src -m pytest . && coverage xml
```

### Updating lock file

When updating Poetry's lock file your local cache can become outdated.
You can clear your cache with `poetry cache clear PyPI --all`
