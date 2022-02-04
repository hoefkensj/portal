
#!/usr/bin/env bash
###
# File:
# ~/.bash/10_includes.bashrc
#
#
### Local
#
[[ -f ~/.bash/20_shopt.bashrc ]] 		&& . ~/.bash/20_shopt.bashrc
[[ -f ~/.bash/30_functions.bashrc ]] 	&& . ~/.bash/30_functions.bashrc
[[ -f ~/.bash/40_variables.bashrc ]] 	&& . ~/.bash/40_variables.bashrc
[[ -f ~/.bash/50_aliases.bashrc ]] 		&& . ~/.bash/50_aliases.bashrc
[[ -f ~/.bash/51_aliases_arco.bashrc ]] && . ~/.bash/51_aliases_arco.bashrc
[[ -f ~/.bash/60_exports.bashrc ]]      && . ~/.bash/60_exports.bashrc
#
###	System
#
[[ -r /usr/share/bash-completion/bash_completion ]] && . /usr/share/bash-completion/bash_completion
#
# File:
# ~/.bash/10_includes.bashrc
###
