
PATH_TO_CONFIG="$HOME/.config/qtile"

picom \
  		--config "$PATH_TO_CONFIG/conf/picom.conf" \
  		--experimental-backends \
  		-b
