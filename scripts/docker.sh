#!/bin/bash

docker run --platform linux/amd64 --rm -it -p 4000:4000 -v ${PWD}:/srv/jekyll jekyll/jekyll jekyll serve
