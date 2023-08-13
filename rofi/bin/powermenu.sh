#!/usr/bin/env bash

styles="$(dirname $(which $0))/../styles"
rofi_command="rofi -theme $styles/powermenu.rasi"

#### Options ###
shutdown=""
reboot=""
lock=""
suspend=""
logout="󰗼"

options="$shutdown\n$reboot\n$lock\n$suspend\n$logout"

uptime=$(uptime | sed -e 's/up //g')

confirm_exit() {
	"$(dirname $(which $0))/confirm.sh"
}

# Message
msg() {
	rofi -theme "$styles/message.rasi" -e "Available Options  -  yes / y / no / n"
}

chosen="$(echo -e "$options" | $rofi_command -p "󱎫  $uptime " -dmenu -selected-row 2)"
case $chosen in
$lock)
	if [[ -f $HOME/bin/lock ]]; then
		$HOME/bin/lock
	elif [[ -f /usr/bin/i3lock ]]; then
		i3lock
	elif [[ -f /usr/bin/dm-tool ]]; then
		dm-tool "lock"
	fi
	;;
$shutdown)
	ans=$(confirm_exit &)
	if [[ $ans == "yes" ]]; then
		systemctl poweroff
	elif [[ $ans == "no" ]]; then
		exit 0
	else
		msg
	fi
	;;
$reboot)
	ans=$(confirm_exit &)
	if [[ $ans == "yes" ]]; then
		systemctl reboot
	elif [[ $ans == "no" ]]; then
		exit 0
	else
		msg
	fi
	;;
$suspend)
	ans=$(confirm_exit &)
	if [[ $ans == "yes" ]]; then
		mpc -q pause
		amixer set Master mute
		systemctl suspend
	elif [[ $ans == "no" ]]; then
		exit 0
	else
		msg
	fi
	;;
$logout)
	ans=$(confirm_exit &)
	if [[ $ans == "yes" || $ans == "y" ]]; then
		loginctl terminate-session ${XDG_SESSION_ID-}
	elif [[ $ans == "no" || $ans == "n" ]]; then
		exit 0
	else
		msg
	fi
	;;
esac
