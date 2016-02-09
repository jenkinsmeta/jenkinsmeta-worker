#!/usr/bin/env bash

git config user.name "Jenkinsmeta CI"
git config user.email "mkasprzyk@szy.fr"

git clone https://github.com/jenkinsmeta/jenkinsmeta-docker.git

cd jenkinsmeta-docker  
echo "Update submodules..."
git submodule foreach git pull origin master
echo "Commit changes..."
git commit -m 'Update submodules'
echo "Push them all!"
git push origin master
cd -
