#!/bin/bash -x
# this script runs the normal monkey in production environment

SERVER_ADDRESS=http://localhost:8000
FOREVER_PATH=/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever
PROJECT_DIR=/home/ec2-user/LWW-Element-Set-App
PROJECT_NAME=normal_monkey
NORMAL_MONKEY_MAX_DELAY_SECONDS=5

echo "Initiating normal monkey deployment ..."

echo "Stopping current deployment"
$FOREVER_PATH stop $PROJECT_NAME

echo "Go to project directory"
cd $PROJECT_DIR

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Starting normal monkey..."
NORMAL_MONKEY_MAX_DELAY_SECONDS=$NORMAL_MONKEY_MAX_DELAY_SECONDS \
    SERVER_ADDRESS=$SERVER_ADDRESS $FOREVER_PATH start \
    --uid $PROJECT_NAME --append -c "python $PROJECT_DIR/monkeys/normal.py" .

echo "Deployment complete"