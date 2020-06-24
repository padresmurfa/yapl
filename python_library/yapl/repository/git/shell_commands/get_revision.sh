#!/bin/bash

# exit immediately upon error
set -e

PATH_TO_CHECK=$1

pushd "$PATH_TO_CHECK" >/dev/null
git rev-parse HEAD
popd >/dev/null
