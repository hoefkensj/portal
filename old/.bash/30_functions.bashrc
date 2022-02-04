#!/usr/bin/env bash
############
# File:
# ~/.bash/30_functions.bashrc
# 
#
#
########
# functions: includes
# 
# include functions related to history 
[[ -f ~/.bash/31_functions_history.bashrc ]] 		&& . ~/.bash/31_functions_history.bashrc
# include functions related to  terminal colors 
[[ -f ~/.bash/32_functions_colors.bashrc ]] 		&& . ~/.bash/32_functions_colors.bashrc
# include function: mini programn :extract 
[[ -f ~/.bash/33_functions_extract.bashrc ]] 		&& . ~/.bash/33_functions_extract.bashrc
#
#
########
########
# functions: functions
#
# function: open files for editing
_open_files_for_editing() {
    # Open any given document file(s) for editing (or just viewing).
    # Note1:
    #    - Do not use for executable files!
    # Note2:
    #    - Uses 'mime' bindings, so you may need to use
    #      e.g. a file manager to make proper file bindings.

    if [ -x /usr/bin/exo-open ] ; then
        echo "exo-open $@" >&2
        setsid exo-open "$@" >& /dev/null
        return
    fi
    if [ -x /usr/bin/xdg-open ] ; then
        for file in "$@" ; do
            echo "xdg-open $file" >&2
            setsid xdg-open "$file" >& /dev/null
        done
        return
    fi

    echo "$FUNCNAME: package 'xdg-utils' or 'exo' is required." >&2
}
# function:  Window Title
# Change the window title of X terminals
function window_title()
{
	case ${TERM} in
		xterm*|rxvt*|Eterm*|aterm|kterm|gnome*|interix|konsole*)
			PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\007"'
			;;
		screen*)
			PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\033\\"'
			;;
	esac
}
# function: ??????
function _set_liveuser_PS1()
{
    PS1='[\u@\h \W]\$ '
    if [ "$(whoami)" = "liveuser" ] ; then
        local iso_version="$(grep ^VERSION= /usr/lib/endeavouros-release 2>/dev/null | cut -d '=' -f 2)"
        if [ -n "$iso_version" ] ; then
            local prefix="eos-"
            local iso_info="$prefix$iso_version"
            PS1="[\u@$iso_info \W]\$ "
        fi
    fi
}
# funtion: Installer Info
function ShowInstallerIsoInfo()
{
    local file=/usr/lib/endeavouros-release
    if [ -r $file ] ; then
        cat $file
    else
        echo "Sorry, installer ISO info is not available." >&2
    fi
}
########
# functions: Executes
#
_set_liveuser_PS1
window_title
#
########
#############
#
# File:
# ~/.bash/30_functions.bashrc
#
##############
