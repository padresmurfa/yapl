#!/bin/bash

# exit immediately upon error
set -e

DIR_IN_REPOSITORY=$1

pushd "$DIR_IN_REPOSITORY" >/dev/null
git rev-parse HEAD
popd >/dev/null
