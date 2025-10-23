#!/bin/bash

DIRS=(
    "$HOME"
    "$HOME/Code"
    "$HOME/.config"
)

if [[ $# -eq 1 ]]; then
    selected=$1
else
    selected=$(fd . "${DIRS[@]}" --type=dir --max-depth=1 --full-path --unrestricted \
        | sed "s|^$HOME/||" \
        | cat - <(echo "home") \
        | sk --margin 10% --color="bw")
    [[ $selected ]] && selected="$HOME/$selected"
fi

[[ ! $selected ]] && exit 0

selected_name=$(basename "$selected" | tr . _)
if ! tmux has-session -t "$selected_name"; then
    tmux new-session -ds "$selected_name" -c "$selected"

    tmux new-window -t "$selected_name:2" -c "$selected" nvim .
    if [ -d "$selected/.git" ]; then
        tmux new-window -t "$selected_name:3" -c "$selected" lazygit
    elif [[ $selected == *".config"* ]]; then
        tmux new-window -t "$selected_name:3" lazygit -ucd ~/.local/share/yadm/lazygit -w ~ -g ~/.local/share/yadm/repo.git
    fi

    tmux select-window -t "$selected_name:1"
fi

tmux switch-client -t "$selected_name"
