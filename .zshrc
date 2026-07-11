unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
esac

fortune | cowsay -f moose
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export ZSH="$HOME/.oh-my-zsh"
# Use different ZSH custom folder so we can use git submodules to track plugins
export ZSH_CUSTOM="$HOME/.config/.oh-my-zsh"

zstyle ':omz:update' mode auto      # update automatically without asking
zstyle ':completion:*' completer _expand_alias _complete _ignored

ENABLE_CORRECTION="true"

COMPLETION_WAITING_DOTS="true"

plugins=(
  git
  git-open
)

if [[ $machine = "Linux" ]]; then
  plugins+=('zsh-archlinux')
fi

if [ -f "$ZSH/oh-my-zsh.sh" ]; then
  source $ZSH/oh-my-zsh.sh
fi

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

export MANGOHUD=1
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/bin/site_perl:/usr/bin/vendor_perl:/usr/bin/core_perl:/usr/lib/rustup/bin:$HOME/.local/bin:$PATH

# make ctrl + backspace = delete word
bindkey ^h backward-delete-word

# Enable dark themes
export GTK_THEME=Adwaita:dark
export GTK2_RC_FILES=/usr/share/themes/Adwaita-dark/gtk-2.0/gtkrc
export QT_STYLE_OVERRIDE=adwaita-dark

source ~/.alias
autoload bashcompinit
bashcompinit

export DEVKITPRO=/opt/devkitpro
export DEVKITARM=/opt/devkitpro/devkitARM
export DEVKITPPC=/opt/devkitpro/devkitPPC

export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt6/plugins/platforms #fix for slippi

export EDITOR=nvim

eval "$(zoxide init --cmd cd zsh)"

CORRECT_IGNORE_FILE='.*'

THEME="/usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme"
if [ -f "$THEME" ]; then
  source $THEME
fi

AUTOSUGGEST="/usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh"
if [ -f "$AUTOSUGGEST" ]; then
  source $AUTOSUGGEST
fi

HIGHLIGHTING="/usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
if [ -f "$HIGHLIGHTING" ]; then
  source $HIGHLIGHTING
fi

if command -v tmux &>/dev/null && [ -z "$TMUX" ]; then
  tmux attach-session -t home || tmux new-session -s home
fi

