#!/bin/bash
picom &

xset s -dpms
xset s off

qtile cmd-obj -o cmd -f reload_config

/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &

clipcatd &

# Get automatic location for redshift
/usr/lib/geoclue-2.0/demos/agent &
redshift &

discord &
steam-runtime &
kitty &

seventeenlands &
export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt6/plugins/platforms #fix for slippi
