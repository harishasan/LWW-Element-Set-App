if [ -z ${IS_PRODUCTION+x} ];
    then echo "running all local modules";
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    sh $DIR/run/start_server_local.sh &
    sh $DIR/run/start_monkey_normal_local.sh &
    sh $DIR/run/start_monkey_offline_to_online_local.sh &
    sh $DIR/run/start_monkey_client_viewer_local.sh &
else
    echo "running on prod";
    FOREVER_PATH=/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever
    $FOREVER_PATH stopall
    sh $DIR/run/start_server_production.sh &
    sh $DIR/run/start_monkey_normal_production.sh &
    sh $DIR/run/start_monkey_offline_to_online_production.sh &
    sh $DIR/run/start_monkey_client_viewer_production.sh &
fi
