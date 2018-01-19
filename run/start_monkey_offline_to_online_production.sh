#!/bin/bash -x

echo "Initiating offline to online monkey deployment ..."

echo "Stopping current deployment"
/usr/bin/forever stop offline_to_online

echo "Go to project directory"
cd /home/ec2-user/LWW-Element-Set-App

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Set environment variables..."
export SERVER_ADDRESS=http://localhost:8000
export OFFLINE_TO_ONLINE_MONKEY_MAX_DELAY_SECONDS=5

echo "Starting normal monkey..."
/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever start --uid "offline_to_online" --append -c "python ./monkeys/offline_to_online.py" .

echo "Deployment complete"