#!/bin/bash -x

echo "Initiating client viewer monkey deployment ..."

echo "Stopping current deployment"
/usr/bin/forever stop client_viewer

echo "Go to project directory"
cd /home/ec2-user/LWW-Element-Set-App

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Set environment variables..."
export SERVER_ADDRESS=http://localhost:8000

echo "Starting normal monkey..."
/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever start --uid "client_viewer" --append -c "python ./monkeys/client_viewer.py" .

echo "Deployment complete"