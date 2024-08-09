#!/usr/bin/env bash

dotnet build
poetry install --no-interaction --no-root
poetry run pip install -e .
poetry run pre-commit install-hooks
