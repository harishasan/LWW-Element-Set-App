#!/bin/bash -x
# This scripts launches following modules
# the server app
# normal monkey
# offline to online monkey
# client viewer monkey
#
# Script works for both local and production enviroment.
# Script assumes it is production environment if IS_PRODUCTION variable is set in environment
# stopping the terminal will end the server and disconnect all the monkeys.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FOREVER_PATH=/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever

if [ -z ${IS_PRODUCTION+x} ];
    then echo "running all modules in local environment";

    # launches monkeys after 2 seconds of launching server
    (sleep 2; sh $DIR/run/start_monkey_normal_local.sh) &
    (sleep 2; sh $DIR/run/start_monkey_offline_to_online_local.sh) &
    (sleep 2; sh $DIR/run/start_monkey_client_viewer_local.sh) &
    sh $DIR/run/start_server_local.sh
else
    echo "running on prod";

    $FOREVER_PATH stopall
    sh $DIR/run/start_server_production.sh &
    sleep 5
    sh $DIR/run/start_monkey_normal_production.sh &
    sleep 5
    sh $DIR/run/start_monkey_offline_to_online_production.sh &
    sleep 5
    sh $DIR/run/start_monkey_client_viewer_production.sh &
    sleep 5
fi
