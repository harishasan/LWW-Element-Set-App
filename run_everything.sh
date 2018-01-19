# just a small script for convenience

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FOREVER_PATH=/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever

if [ -z ${IS_PRODUCTION+x} ];
    then echo "running all local modules";

    sh $DIR/run/start_server_local.sh &
    sh $DIR/run/start_monkey_normal_local.sh &
    sh $DIR/run/start_monkey_offline_to_online_local.sh &
    sh $DIR/run/start_monkey_client_viewer_local.sh &
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
