#!/bin/bash

# Build image if image not exists
if [[ "$(docker images -q spacy-ails:latest 2> /dev/null)" == "" ]]; then
    docker build -t spacy-ails:latest .
fi

docker run -t -p 1234:80 spacy-ails 
