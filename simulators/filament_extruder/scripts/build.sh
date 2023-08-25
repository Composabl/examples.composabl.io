#!/bin/bash
APP_NAME=${1:-"sim-gymnasium"}

if [ -z "$APP_NAME" ]; then
    echo "Please provide the name of the container"
    echo "Usage: ./build.sh <APP_NAME>"
    exit 1
fi

REPO="composabl.ai"
TAG=$(date +%Y%m%d%H%M%S) # alternatively: git log -1 --pretty=%H 

# 0. Build the wheel for the SDK
echo "Building the wheel for the SDK"
CURR_DIR=$(pwd)
cd ../../composabl/sdks/python_sdk
poetry build
cd "$CURR_DIR"

echo "Copying the wheel to the docker build context"
cp -r ../../composabl/sdks/python_sdk/dist/*.whl ./docker

# 1. Build and Push
echo "Building the docker container"
docker buildx build --platform linux/amd64 --progress plain -t "$REPO/$APP_NAME:$TAG" -t "$REPO/$APP_NAME:latest" . 