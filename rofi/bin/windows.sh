#!/bin/bash

styles="$(dirname $(which $0))/../styles"
rofi -show window -theme $styles/launcher.rasi
