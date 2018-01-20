#!/bin/bash -x
# this script runs the client viewer monkey in development environment

export SERVER_ADDRESS=http://localhost:8000
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../monkeys/client_viewer.py