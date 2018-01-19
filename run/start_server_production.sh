#!/bin/bash -x

PORT=8000
PERSISTENCE_PATH=/home/ec2-user/goodnotes.db
FOREVER_PATH=/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever

echo "Initiating server deployment ..."

echo "Stopping current deployment"
/usr/bin/forever stop master
fuser -k $PORT/tcp

echo "Go to project directory"
project_dir=/home/ec2-user/LWW-Element-Set-App
cd $project_dir

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Set environment variables..."

echo "Starting python server ..."
PORT=$PORT PERSISTENCE_PATH=$PERSISTENCE_PATH $FOREVER_PATH start --uid "server" --append -c "python $project_dir/server/index.py" .

echo "Deployment complete"
