#!/bin/bash -x

echo "Initiating normal monkey deployment ..."

echo "Stopping current deployment"
/usr/bin/forever stop normal_monkey

echo "Go to project directory"
cd /home/ec2-user/LWW-Element-Set-App

echo "Pull latest code ..."
git pull origin master

echo "Install dependencies ..."
pip install -r requirements.txt

echo "Set environment variables..."
export SERVER_ADDRESS=http://localhost:8000
export NORMAL_MONKEY_MAX_DELAY_SECONDS=5

echo "Starting normal monkey..."
/home/ec2-user/.nvm/versions/node/v9.4.0/bin/forever start --uid "normal_monkey" --append -c "python ./monkeys/normal.py" .

echo "Deployment complete"