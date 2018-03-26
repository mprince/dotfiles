#!/usr/bin/env bash

PROJECTS_ROOT=~/projects
cd $PROJECTS_ROOT
#projects=$(ls -d */ | sed -e "s/\///g") # ls -d */ | sed -e "s/\///g" OR echo */ OR ls -F | grep /
projects="" # projects array

for project in $projects; do
    cd $PROJECTS_ROOT\/$project
    git checkout master && git pull upstream master && git push origin master
    git checkout release-next && git pull upstream release-next && git push origin release-next
#    if [ -d .git ]; then
#        git remote -v | awk '{print $1}' | uniq
#        echo "NEXT"
#    fi;
done
