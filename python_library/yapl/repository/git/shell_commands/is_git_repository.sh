#!/bin/bash

PATH_TO_CHECK=$1

pushd "$PATH_TO_CHECK" >/dev/null || exit 1
git rev-parse --show-toplevel >/dev/null 2>/dev/null
RESULT=$?
popd >/dev/null || exit 1

if [ "$RESULT" == "0" ];
then
  echo "yes"
else
  echo "no"
fi
