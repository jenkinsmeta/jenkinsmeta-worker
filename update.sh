#!/usr/bin/env bash

git config --global user.name "Jenkinsmeta CI"
git config --global user.email "mkasprzyk@szy.fr"

git clone https://github.com/jenkinsmeta/jenkinsmeta-docker.git

cd jenkinsmeta-docker  
echo "Update submodules..."
git submodule init
git submodule update
git submodule foreach git pull origin master
echo "Commit changes..."
git commit -am 'Update submodules'
echo "Push them all!"
git push --force "https://${GH_TOKEN}@${GH_REF}" master:master
cd -
