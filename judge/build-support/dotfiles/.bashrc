# Terminal colors
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

if [ -f ~/.git-completion ]; then
  . ~/.git-completion
fi

if [ -f ~/.git-prompt ]; then
  source ~/.git-prompt
fi

# Color prompt with Git branch and Python virtualenv support
function posh_git_prompt {
    local pg_location="\[\033[01;34m\][\w]"
    local pg_virtualenv='`if [ ! -z "$VIRTUAL_ENV" ]; then echo "\[\033[33m\] (venv: $(basename $VIRTUAL_ENV))"; fi`'
    local pg_user_hostname="\[\033[01;32m\]\u@\h"
    local pg_prompt="\[\033[35m\]$\[\033[00m\]"
    local pg_full_prompt="\n$pg_location$pg_virtualenv\n$pg_user_hostname $pg_prompt"
    export PROMPT_COMMAND="__git_ps1 \"$pg_full_prompt\" \" \";"$PROMPT_COMMAND
}

posh_git_prompt

# Command aliases
alias ls="ls -G --color"
alias lsa="ls -lAG --color"
