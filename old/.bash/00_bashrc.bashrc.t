#!/usr/bin/env bash
############
# File:
# ~/.bash/00_bashrc.bashrc
# 
#
#
########
# bashrc: Includes
#
# 
[[ -f ~/.bash/10_includes.bashrc ]] && . ~/.bash/10_includes.bashrc
#
#
########
#
########
# bashrc: 
# 
#
# If not running interactively, don't do anything
[[ $- != *i* ]] && return

#
#PROMPT_COMMAND=_bash_history_sync
use_color=true
xhost +local:root > /dev/null 2>&1
#
#
########
#
########
# functions: Executes
#
window_title
PROMPT_COMMAND=_bash_history_sync 
#
#
########
#
#
#############
#
# File:
# ~/.bash/00_bash.bashrc
#
##############
