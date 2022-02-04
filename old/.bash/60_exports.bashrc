export PYTHONPATH="/usr/local/lib/python3.10/site-packages:/home/hoefkens/Development/Python:$PYTHONPATH"

export MICRO_TRUECOLOR=1

[[ -z "$FUNCNEST" ]] && export FUNCNEST=100          # limits recursive functions, see 'man bash'
