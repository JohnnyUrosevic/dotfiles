#!/bin/bash
picom &
xrandr -d DP-3 -s 1920x1080 -r 144
xrandr -d HDMI-1 -s 1920x1080 -r 60
xset s -dpms
xset s off
nitrogen --restore
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
redshift