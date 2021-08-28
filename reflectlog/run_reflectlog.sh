#!/bin/bash

run_dir=$(pwd)
dir="$(realpath "${0}" | xargs dirname)"
logdir=$dir/../logs
mkdir -p $logdir

. $dir/../venv/py3/bin/activate

python3 $dir/main.py --ics="$ICS" \
  --git_log_dir="$logdir"
