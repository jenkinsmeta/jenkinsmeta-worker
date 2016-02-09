#!/usr/bin/env bash

git config user.name "Jenkinsmeta CI"
git config user.email "mkasprzyk@szy.fr"

git clone https://github.com/jenkinsmeta/jenkinsmeta-docker.git

cd jenkinsmeta-docker  
git submodule foreach git pull origin master
#git commit -m 'Update submodules'
#git push origin master
cd -

