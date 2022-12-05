#!/usr/bin/env bash

styles="$(dirname $(which $0))/../styles"
rofi -show ssh -theme $styles/launcher.rasi -disable-history -no-parse-known-hosts
