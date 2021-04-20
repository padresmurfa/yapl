#!/bin/bash

# exit immediately upon error
set -e

DIR_IN_REPOSITORY=$1
HASH=$2

pushd "$DIR_IN_REPOSITORY" >/dev/null

git show --no-patch --no-notes --pretty='%cI' "$HASH"

popd >/dev/null

