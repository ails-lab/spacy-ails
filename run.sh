#!/bin/bash


# Build image
if [[ "$(docker images -q spacy-ails:latest 2> /dev/null)" != "" ]]; then
    docker stop spacy-ails
    docker rm spacy-ails
    docker rmi spacy-ails:latest
fi

docker build -t spacy-ails .
docker run -d --name spacy-ails -p 80:80 spacy-ails