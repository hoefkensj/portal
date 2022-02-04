#!/bin/bash
#
# File:
# ~/.bash/aliasses_ARCO.bashrc
##

alias rebash='source ~/.bash_profile'


alias ll='ls -bghAls'
alias llr='ls -bRghAls'
alias rmr="rm -r"
alias rmrf="sudo rm -rf"
alias frqmax='sudo cpupower frequency-set -g performance'
alias frqmin='sudo cpupower frequency-set -g powersave'
alias frqinfo='sudo cpupower frequency-info'

#alias cp="cp -iv"                          # confirm before overwriting something
alias df='df -h'                          # human-readable sizes
alias free='free -m'                      # show sizes in MB
alias np='micro -w PKGBUILD'
#alias more=less
alias du='du -hc'
alias du-s='du -hcs'

alias yas='yay -Ss'
alias yayy='yay --noconfirm'

alias b-du='sudo btrfs file du --human-readable -s'
#alias b-df=''
alias b-s='sudo btrfs subv'     #= btrfs subvolume $
alias lsbs='sudo btrfs subv list' #= btrfs subvolume list $
alias ddbs='btrfs subv snapshot' #= btrfs subvolume duplicate  $
alias mkbs='btrfs subv create' #= btrfs subvolume create $
alias rmbS='btrfs subv delete' #= btrfs subvolume delete $

alias b-f='sudo btrfs file'    #= btrfs filesystem $

#systemctl
alias sctl="sudo systemctl"
alias sctls="sudo systemctl start"
alias sctlp="sudo systemctl stop"
alias ntfixall="lsblk -o FSTYPE,PATH  | awk '$1 == \"ntfs\" {print $2}'"



alias pycharm="/opt/JetBrains/apps/PyCharm-C/ch-0/203.7717.81/bin/pycharm.sh &"
alias ccat='ccat --bg="dark" -G Decimal="*green*" -G Keyword="blue" -G Punctuation="*yellow*" -G Plaintext="reset" -G String="brown" -G Type="*white*" -G Literal="fuchsia"'
