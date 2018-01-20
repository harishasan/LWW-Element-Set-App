#!/bin/bash -x
# this script runs the server app in development environment

export PORT=8000
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PERSISTENCE_PATH=$DIR/../goodnotes.db
python $DIR/../server/index.py