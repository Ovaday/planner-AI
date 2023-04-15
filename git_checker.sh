#!/bin/sh

git remote update | grep "hide output"

UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
    echo "Need to pull"
    sudo systemctl stop qcluster.service
    git pull
    /home/ubuntu/planner-AI/virt_env/bin/pip install -r requirements.txt
    sudo systemctl start qcluster.service
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi