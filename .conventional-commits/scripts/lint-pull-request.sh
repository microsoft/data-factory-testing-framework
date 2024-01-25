#!/bin/sh
set -e
PR_TITLE="$1"
PR_BODY="$2"
COMMIT_LINT_CONFIG="$3"

npm install -g @commitlint/cli@17 @commitlint/config-conventional@17

echo "$PR_TITLE\n\n$PR_BODY" | commitlint --config "$COMMIT_LINT_CONFIG" --verbose
