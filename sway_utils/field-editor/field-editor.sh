#!/bin/bash

# shellcheck disable=SC1090
source "$HOME/.config/base16-shell/scripts/base16-default-dark.sh"

if test -n "$1"; then
    sleep .02
    swaymsg "resize set 700px 975px"
    vim --cmd "let g:gitgutter_enabled=0" $1
else
    echo "error: no filename provided"
fi
