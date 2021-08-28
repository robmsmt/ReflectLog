#!/bin/bash

dir="$(realpath "${0}" | xargs dirname)"
logdir=$dir/../logs
mkdir -p $logdir
cd $logdir
git init
echo -n "What is your PRIVATE github URL (e.g: git@github.com:robmsmt/MyPersonalLog.git): "
read answer
git remote add origin $answer
touch README.md
git add .
git commit -m "first init"
git push --set-upstream origin master