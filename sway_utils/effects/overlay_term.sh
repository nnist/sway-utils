alacritty \
    --option font.size=24 \
    window.dimensions.columns=20 \
    window.dimensions.lines=7 \
    colors.cursor.cursor=\"CellBackground\" \
    colors.cursor.text=\"CellBackground\" \
    cursor.style=\"Underline\" \
    background_opacity=0.0 \
    --class=overlay \
    -e /bin/bash -c "source $HOME/.config/base16-shell/scripts/base16-default-dark.sh; tput civis; $1"
