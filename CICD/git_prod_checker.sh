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

    sudo systemctl stop qcluster.prod.service
    git stash --include-untracked
    git pull
    source /home/ubuntu/planner-AI-prod/virt_env/bin/activate
    pip install -r /home/ubuntu/planner-AI-prod/requirements.txt
    deactivate
    sudo systemctl start qcluster.prod.service
elif [ $REMOTE = $BASE ]; then
    echo "Need to push"
else
    echo "Diverged"
fi