alias sc='echo -e "\nMy shortcuts: \n"; cat ~/.bash_aliases;'

###-----Docker-----###
alias drm="docker ps -a | grep Exit | cut -d ' ' -f1 | xargs docker rm"

###-----Git-----###
alias gs="git status"
alias gl="git log"
alias gb="git branch"
alias gd="git diff"
alias gc="git commit"
alias gp="git pull"
alias gcp="git cherry-pick"
alias gr="git remote"
alias grb="git rebase"
#alias rn="co release-next && git pull upstream release-next"
#alias ms="co master && git pull upstream master"
alias stash="git stash"
alias pop="git stash pop"
alias poo="git checkout -- regression/pool-1-thread-1.properties"
alias uncommit="git reset --soft HEAD^"
alias gm="git merge --no-ff"
alias gi="git checkout --"
alias gca="gc -a --amend --no-edit"
alias co="git checkout"
#current_branch=$(git symbolic-ref --short -q HEAD)
#gcom () { git commit -am "$current_branch: $1";}
#gpush () { git push origin $1;}
#co () { git checkout $1;}
#cob () { git checkout -b $1;}
#gdel () { git branch -d $1;}
#gDel () { git branch -D $1;}

###-----Jenkins & Salt-----###
#alias jobdsl='java -jar /<path_to_dir>/job-dsl-plugin-job-dsl-1.59/job-dsl-core/build/libs/job-dsl-core-1.59-standalone.jar'
#alias highstate='salt-call state.highstate --state-output=mixed'

###-----Codeception-----###
#alias ceptowl='/<path_to_dir>/vendor/bin/codecept'
#alias ceptbuild='ceptowl build --config=/<path_to_dir>/codeception/'
#alias ceptrunfun='ceptowl run functional --config=/<path_to_dir>/codeception/ -vv'
#alias ceptclean='ceptowl clean --config=/<path_to_dir>/codeception/'
#ceptrun () { ceptowl run functional /<path_to_dir>/codeception/tests/functional/$1 --config=/<path_to_dir>/codeception/ -vv $2;}
#ceptrung () { ceptowl run functional /<path_to_dir>/codeception/tests/functional/$1 --config=/<path_to_dir>/codeception/ -vv $2 -g $3;}

#-----alias working with directory-----
alias cdproj="cd ~/projects"
alias ll='ls -la | grep "^d" && ls -la | grep -v "^d"'

###-----Others-----###
alias chrome="/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"

