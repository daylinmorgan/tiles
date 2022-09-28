#!/usr/bin/env bash

styles="$(dirname $(which $0))/../styles"
rofi_command="rofi -theme $styles/confirm.rasi"

options="yes\nno"

chosen="$(echo -e "$options" | $rofi_command -dmenu -selected-row 2)"
echo "$chosen"
