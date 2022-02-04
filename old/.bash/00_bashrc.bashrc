#
# ~/.bashrc
#
#
########
# Dont do anything if not interactivel:
#
[[ $- != *i* ]] && return
#
#
########
# name: includes
#
[[ -f ~/.bash/10_includes.bashrc ]] && . ~/.bash/10_includes.bashrc
#
#
########
# BODY
xhost +local:root > /dev/null 2>&1
####
########
# executes
#
PROMPT_COMMAND=_bash_history_sync
[[ -f ~/.welcome_screen ]] && . ~/.welcome_screen

unset -f _set_liveuser_PS1

[[ "$(whoami)" = "root" ]] && return
[[ -z "$FUNCNEST" ]] && export FUNCNEST=100          # limits recursive functions, see 'man bash'

## Use the up and down arrow keys for finding a command in history
## (you can write some initial letters of the command first).
bind '"\e[A":history-search-backward'
bind '"\e[B":history-search-forward'
bind 'set completion-ignore-case on'
# alias ef='_open_files_for_editing'     # 'ef' opens given file(s) for editing
# alias pacdiff=eos-pacdiff
################################################################################

### Bashhub.com Installation.
### This Should be at the EOF. https://bashhub.com/docs
if [ -f ~/.bashhub/bashhub.sh ]; then
    source ~/.bashhub/bashhub.sh
fi

