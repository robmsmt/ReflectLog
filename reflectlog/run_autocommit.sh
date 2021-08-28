#!/bin/bash

dir="$(realpath "${0}" | xargs dirname)"
logdir=$dir/../logs
mkdir -p $logdir
cd $logdir

date=$(date +%Y%m%d_%H%M%S)
git pull origin
git add .
git commit -m "$date"
git push origin