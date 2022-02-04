#!/bin/bash
#
# File:
# ~/.bash/shopt.bashrc
##
shopt -s extglob
# Bash won't get SIGWINCH if another process is in the foreground.
# Enable checkwinsize so that bash will check the terminal size when
# it regains control.  #65623
# http://cnswww.cns.cwru.edu/~chet/bash/FAQ (E11)
shopt -s checkwinsize
# expand aliasses in .bash/aliases.bashrc
shopt -s expand_aliases
# enable * wildcard includes .-files (ex: rm ~/tmp/* removes .test and test |fix for .* wich includes ..)
shopt -s dotglob
## reedit a history substitution line if it failed
shopt -s histreedit
## edit a recalled history line before executing
shopt -s histverify
# Enable history appending instead of overwriting.  #139609
shopt -s histappend
# change to named directory
shopt -s autocd 
# autocorrects cd misspellings
shopt -s cdspell
# save multi-line commands in history as single line 
shopt -s cmdhist
# no Case globbing
shopt -s nocaseglob
# file: ~/.bash/shopt.bashrc
