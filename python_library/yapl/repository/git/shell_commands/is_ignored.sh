#!/bin/bash

DIR_IN_REPOSITORY=$1
PATH_TO_CHECK=$2

pushd "$DIR_IN_REPOSITORY" >/dev/null || exit 1
git check-ignore "$PATH_TO_CHECK" >/dev/null
RESULT=$?
popd >/dev/null || exit 1

if [ "$RESULT" == "0" ];
then
  echo "yes"
else
  echo "no"
fi
