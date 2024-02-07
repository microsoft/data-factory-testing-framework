#!/bin/sh
set -e
PR_TITLE="$1"
COMMIT_LINT_CONFIG="$2"

npm install -g @commitlint/cli@17 @commitlint/config-conventional@17

echo "$PR_TITLE" | commitlint --config "$COMMIT_LINT_CONFIG" --verbose
