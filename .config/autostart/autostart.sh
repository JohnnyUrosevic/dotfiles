#!/bin/bash
picom &

xset s -dpms
xset s off

qtile cmd-obj -o cmd -f reload_config

/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &

clipcatd &

redshift -l '34.05:-118.15' -t '6500:2500' &

discord &
steam &
1password --silent &
obsidian &
kitty &

seventeenlands &
