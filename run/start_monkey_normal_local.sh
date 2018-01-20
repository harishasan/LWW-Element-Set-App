#!/bin/bash -x
# this script runs the normal monkey in development environment

export SERVER_ADDRESS=http://localhost:8000
export NORMAL_MONKEY_MAX_DELAY_SECONDS=5
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../monkeys/normal.py