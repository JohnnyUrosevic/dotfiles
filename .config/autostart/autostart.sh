#!/bin/bash
picom &

xrandr --output DP-1 -s 2560x1440 -r 170 --auto
xrandr --output DP-3 --right-of DP-1 -r 144 --auto
xset s -dpms
xset s off

/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &

clipcatd &

# Get automatic location for redshift
/usr/lib/geoclue-2.0/demos/agent &
redshift &

discord &