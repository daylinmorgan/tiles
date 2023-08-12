#!/usr/bin/env bash

COLORSCRIPT="$HOME/.config/qtile/colors.py"
styles="$(dirname $(which $0))/../styles"

rofi -show color -modes "color:$COLORSCRIPT" -theme "$styles/launcher.rasi"
