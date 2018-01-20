#!/bin/bash -x
# this script runs the client viewer monkey in production environment

SERVER_ADDRESS=http://localhost:8000
FOREVER_PATH=/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever
PROJECT_DIR=/home/ec2-user/LWW-Element-Set-App
PROJECT_NAME=client_viewer

echo "Initiating client viewer monkey deployment ..."

echo "Stopping current deployment"
$FOREVER_PATH stop $PROJECT_NAME

echo "Go to project directory"
cd $PROJECT_DIR

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Starting normal monkey..."
SERVER_ADDRESS=$SERVER_ADDRESS $FOREVER_PATH start --uid $PROJECT_NAME --append -c \
    "python $PROJECT_DIR/monkeys/client_viewer.py" .

echo "Deployment complete"