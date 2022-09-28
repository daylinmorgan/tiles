#!/usr/bin/env bash

if ! updates_aur=$(($(pikaur -Qua 2>/dev/null | wc -l) - 1)); then
	updates_aur=0
fi

if [ $updates_aur -gt 0 ]; then
	echo "Aur: ${updates_aur}"
fi
