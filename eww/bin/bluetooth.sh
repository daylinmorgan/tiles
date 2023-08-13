#!/bin/sh
if [ "$(bluetoothctl show | grep "Powered: yes" | wc -c)" -eq 0 ]; then
	echo "󰂲"
else
	if [ "$(bluetoothctl devices Connected | wc -c)" -eq 0 ]; then
		echo ""
	else
		echo "󰂱"
	fi
fi
