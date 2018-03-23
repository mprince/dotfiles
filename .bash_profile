#nvm
export NVM_DIR="$HOME/.nvm"
. "/usr/local/opt/nvm/nvm.sh"

#bash-completion
[ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion

#Git Aware Propmt
export GITAWAREPROMPT=~/.bash/git-aware-prompt
source "${GITAWAREPROMPT}/main.sh"
export PS1="\u \w \[$bldblu\]\$git_branch\[$bldred\]\$git_dirty\[$txtrst\]\$ "
export SUDO_PS1="\[$bakred\]\u@\h\[$txtrst\] \w\$ "

#Maven
export JAVA_HOME=$(/usr/libexec/java_home)
export M2_HOME="/usr/local/Cellar/maven/3.3.9/libexec"
export PATH=$PATH:$JAVA_HOME/bin:$M2_HOME/bin
export MAVEN_OPTS='-Xms512m -XX:MaxPermSize=1024m -Xmx1024m'
export PATH=/usr/local/php5/bin:$PATH

#ulimit -n 1048

#Aliases
source ~/.bash_aliases
