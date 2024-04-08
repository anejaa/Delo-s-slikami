#!/bin/bash
DOCKER_USERNAME="anejaa"
REPO_NAME="delo-s-slikami"
IMAGE_TAG="2024-04-08--14-52-00"

# Prenesi Docker sliko
docker pull $DOCKER_USERNAME/$REPO_NAME:$IMAGE_TAG

# Zaženi Docker vsebnik
docker run -d $DOCKER_USERNAME/$REPO_NAME:$IMAGE_TAG
