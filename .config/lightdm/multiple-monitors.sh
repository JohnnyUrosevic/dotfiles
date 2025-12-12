#!/usr/bin/env bash
xrandr --output HDMI-1 --off --output DP-1 --mode 1920x1080 -r 144 --pos 2560x360 --rotate normal --output DP-2 --primary --mode 2560x1440 -r 170 --pos 0x0 --rotate normal --output HDMI-2 --off --output HDMI-1-3 --off --output DP-1-3 --off --output DP-1-4 --off --output DP-1-5 --off || true

