#!/bin/bash

# exit immediately upon error
set -e

DIR_IN_REPOSITORY=$1
FILENAME=$2

pushd "$DIR_IN_REPOSITORY" >/dev/null
git hash-object "$FILENAME"
popd >/dev/null
