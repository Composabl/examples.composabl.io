#!/bin/bash -e
################################################################################
##  File:  docker.sh
##  Desc:  Installs Docker
################################################################################
# Install docker with the get.docker.com script
# https://github.com/docker/docker-install
curl -fsSL https://get.docker.com | bash

# Allow docker access without sudo
usermod -aG docker $SSH_USER

# Enable docker.service
systemctl is-enabled --quiet docker.service || systemctl enable docker.service
