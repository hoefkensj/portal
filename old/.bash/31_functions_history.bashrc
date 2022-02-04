#!/usr/bin/env bash
#
# File:
# ~/.bash/31_functions_history.bashrc
##
HISTSIZE=9999999999999						#infinit
HISTFILESIZE=$HISTSIZE						# !!
#HISTCONTROL=ignorespace					# dont incl $_[space]_command
HISTLOGDIR="${HOME}/.bash/log"
[[ -d $HISTLOGDIR ]] || mkdir -p $HISTLOGDIR  #create logddir if it doesnt exist
HISTALLFILE="${HOME}/.bash/log/histall.log"


function _bash_history_sync() {
    builtin history -a $HISTFILE      
    builtin history -a $HISTALLFILE       
    HISTFILESIZE=$HISTSIZE    
    builtin history -c         
    builtin history -r         
}

function history() {          
    _bash_history_sync
    builtin history "$@"
}

function histall() {          
    _bash_history_sync
    cat -n $HISTALLFILE    
}

