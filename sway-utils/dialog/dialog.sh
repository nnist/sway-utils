#!/bin/bash
# shellcheck disable=SC1090
source "$HOME/.config/base16-shell/scripts/base16-default-dark.sh"

if test -n "$1"; then
    python3 $HOME/git/sway-utils/sway-utils/dialog/dialog.py "$1" $2 $3 $4
else
    echo "error: no message provided"
    sleep 1
fi
