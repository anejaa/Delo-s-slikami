#!/bin/bash
# Preberi okoljske spremenljivke
DOCKER_USERNAME=$1
DOCKER_PASSWORD=$2
REPO_NAME=$3
IMAGE_TAG=$CURRENT_DATE
# Prijavi se v DockerHub
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

# Zgradi Docker sliko in jo označi z ustrezno oznako
docker build . -f Dockerfile -t $DOCKER_USERNAME/$REPO_NAME:$IMAGE_TAG

# Potisni Docker sliko na DockerHub
docker push $DOCKER_USERNAME/$REPO_NAME:$IMAGE_TAG