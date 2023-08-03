#!/bin/bash
ACR_NAME=$1
APP_NAME=${2:-"sim-gymnasium"}

if [ -z "$ACR_NAME" ]; then
    echo "Please provide the name of the Azure Container Registry"
    echo "Usage: ./deploy.sh <ACR_NAME> [APP_NAME]"
    exit 1
fi

REPO="$ACR_NAME.azurecr.io"
TAG=$(date +%Y%m%d%H%M%S) # alternatively: git log -1 --pretty=%H

# 0. Build the wheel for the SDK
echo "Building the wheel for the SDK"
CURR_DIR=$(pwd)
cd ../../composabl/sdks/python_sdk
poetry build
cd "$CURR_DIR"

echo "Copying the wheel to the docker build context"
cp -r ../../composabl/sdks/python_sdk/dist/*.whl ./docker

# 1. Login to the Container Registry
echo "Logging in to the repository $REPO"
az acr login --name $ACR_NAME

# 2. Build and Push
echo "Building the docker container"
docker buildx build --push --platform linux/amd64 -t "$REPO/$APP_NAME:$TAG" -t "$REPO/$APP_NAME:latest" .

# 3. Deploy the container to the production environment
echo "Deploying the latest version"
echo "Note: this is done through CI/CD on image change. App Service will listen to the ACR webhook and ACR will push to it on each docker push"
