#!/bin/bash
picom &
xrandr -d DP-3 -s 1920x1080 -r 144
xrandr -d HDMI-1 -s 1920x1080 -r 60
xset s -dpms
xset s off
nitrogen --restore
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &

# Get automatic location for redshift
redshift -l $(curl -s "https://location.services.mozilla.com/v1/geolocate?key=geoclue" | awk 'OFS=":" {print $3,$5}' | tr -d ',}')