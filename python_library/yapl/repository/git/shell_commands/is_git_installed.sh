#!/bin/bash

WHICH_GIT=$(command which git)
if [ "$WHICH_GIT" != "" ];
then
  echo "yes"
else
  echo "no"
fi
