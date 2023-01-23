#!/usr/bin/env bash

is-tool() {
	[ -x "$(command -v "$1")" ]
}

PATH_TO_CONFIG="$HOME/.config/qtile"

[ ! -f "$PATH_TO_CONFIG/colors/colors.json" ] && "$PATH_TO_CONFIG/color/colors.py"

for tool in picom eww dunst; do
	pkill $tool &
done

sleep 1

is-tool picom &&
    picom \
 		--config "$PATH_TO_CONFIG/conf/picom.conf" \
 		--experimental-backends \
  	-b \
  		&>/dev/null &
  

is-tool dunst &&
 	cat "$PATH_TO_CONFIG/conf/dunstrc" \
 		"$PATH_TO_CONFIG/colors/dunstrc" | dunst -conf - &

is-tool feh &&
	feh \
		--bg-fill \
		--randomize \
		"$(find -L "${PATH_TO_CONFIG}/wallpapers/current" -type f)" &

eww -c "$PATH_TO_CONFIG/eww daemon" &
# num_monitors=$(($(xrandr --listactivemonitors | wc -l) - 2))
num_monitors=$(echo "scale=0; $(qtile cmd-obj -o cmd -f screens | wc -l) / 10" | bc)
bars=''
for index in $(seq 0 1 "$num_monitors"); do
	bars+="bar$index "
done

# future version on eww won't use open-many
eww -c "$PATH_TO_CONFIG/eww" open-many $bars &
