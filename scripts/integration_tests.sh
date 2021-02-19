#!/bin/bash

docker run -itd -v ${PWD}:/srv/jekyll -p 4000:4000 --name jekyll jekyll/jekyll:latest jekyll serve
sleep 15

python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip pytest bs4 requests
python3 -m pytest
deactivate

rm -rf .venv
docker rm -f jekyll
