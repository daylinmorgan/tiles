#!/usr/bin/env bash

styles="$(dirname $(which $0))/../styles"
rofi -show window -theme $styles/windows.rasi
