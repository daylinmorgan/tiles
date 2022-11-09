#!/usr/bin/env bash

styles="$(dirname $(which $0))/../styles"
rofi -show drun -show-icons -theme $styles/launcher.rasi
