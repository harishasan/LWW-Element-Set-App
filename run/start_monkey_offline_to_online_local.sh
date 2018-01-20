#!/bin/bash -x
# this script runs the offline to online monkey in development environment

export SERVER_ADDRESS=http://localhost:8000
export OFFLINE_TO_ONLINE_MONKEY_MAX_DELAY_SECONDS=5
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../monkeys/offline_to_online.py