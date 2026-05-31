#!/bin/bash
picom &

xset s -dpms
xset s off

xinput set-prop 15 "libinput Accel Profile Enabled Default" 0, 1, 0

wlr-randr --output DP-2 --mode 1920x1080@143.996002 --adaptive-sync disabled --right-of DP-1 --output DP-1 --mode 2560x1440@165 --adaptive-sync disabled --left-of DP-2

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
