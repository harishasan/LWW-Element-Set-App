#!/bin/bash -x
# this script runs the server app in production environment

PORT=8000
PERSISTENCE_PATH=/home/ec2-user/goodnotes.db
FOREVER_PATH=/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever
PROJECT_DIR=/home/ec2-user/LWW-Element-Set-App
PROJECT_NAME=server

echo "Initiating server deployment ..."

echo "Stopping current deployment"
$FOREVER_PATH stop $PROJECT_NAME
fuser -k $PORT/tcp

echo "Go to project directory"
cd $PROJECT_DIR

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Set environment variables..."

echo "Starting python server ..."
PORT=$PORT PERSISTENCE_PATH=$PERSISTENCE_PATH $FOREVER_PATH start \
    --uid $PROJECT_NAME --append -c "python $PROJECT_DIR/server/index.py" .

echo "Deployment complete"
