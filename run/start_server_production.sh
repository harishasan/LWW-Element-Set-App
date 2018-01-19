#!/bin/bash -x

echo "Initiating server deployment ..."

echo "Stopping current deployment"
/usr/bin/forever stop master
fuser -k 8000/tcp

echo "Go to project directory"
cd /home/ec2-user/LWW-Element-Set-App

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Set environment variables..."
export PORT=8000
export PERSISTENCE_PATH=/home/ec2-user/goodnotes.db

echo "Starting python server ..."
/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever start --uid "master" --append -c "python ./../server/index.py" .

echo "Deployment complete"
