#
########
# name: content
# 
######

#
######
# codeblock:title 
#	discription
####
code()
####

#
######
# codeblock:title2
# 	Change the window title of X terminals
####
function window_title(){
        case ${TERM} in
                xterm*|rxvt*|Eterm*|aterm|kterm|gnome*|interix|konsole*)
                        PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\007"'
                        ;;
                screen*)
                        PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\033\\"'
                        ;;
        esac
}
#
######
