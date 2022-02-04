#!/bin/bash
#
# file: 
# ~/.bash/variables.bashrc
###

DEVPY="${HOME}/Development/Python/"
GIT="${HOME}/Development/Git/"
MNTU="/run/media/$USER/"


#WINE DEFAULTS
BTRWin="/mnt/btrd0v1/opt/BTRWin"
WINEARCH="win64"
WINE="${BTRWin}/default/loader"
WINELDR="${WINE}/bin/wine"
WINESVR="${WINE}/bin/wineserver"

BTRWenv="WINEARCH=\"${WINEARCH}\"  WINE=\"${WINELDR}\" WINELOADER=\"${WINELDR}\" WINESERVER=\"${WINESVR}\"  WINEDEBUG=\"-all\"" 

export PATH="/mnt/btrd0v1/opt/BTRWin/default/loader/bin/:$PATH"
# file: ~/.bash/variables.bashrc
