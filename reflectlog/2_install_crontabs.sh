#!/bin/bash

dir=$(pwd)
reflectlog="DISPLAY=:0 $dir/run_reflectlog.sh"
autocommit="$dir/run_autocommit.sh"
echo "Installing crontab pointing to $reflectlog"
crontab -l > mycron
echo "30 18 * * Mon-Fri . $HOME/.ics; $reflectlog > /tmp/reflect.log" >> mycron
echo "00 22 * * Mon-Fri $autocommit > /tmp/reflect_git.log" >> mycron
crontab mycron
rm mycron