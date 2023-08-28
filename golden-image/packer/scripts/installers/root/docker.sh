#!/bin/bash -e
################################################################################
##  File:  docker.sh
##  Desc:  Installs Docker
################################################################################
# Source the helpers for use with the script
source $HELPER_SCRIPTS/os.sh
source $HELPER_SCRIPTS/install.sh

# Configure repo
repo_url="https://download.docker.com/linux/ubuntu"
gpg_key="/usr/share/keyrings/docker.gpg"
repo_path="/etc/apt/sources.list.d/docker.list"

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o $gpg_key
echo "deb [arch=amd64 signed-by=$gpg_key] $repo_url $(getOSVersionLabel) stable" > $repo_path
apt-get update
apt-get install --no-install-recommends -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin

# Install docker compose v2 from releases
URL=$(get_github_package_download_url "docker/compose" "contains(\"compose-linux-x86_64\")")
curl -fsSL $URL -o /usr/libexec/docker/cli-plugins/docker-compose
chmod +x /usr/libexec/docker/cli-plugins/docker-compose

# Enable docker.service
systemctl is-enabled --quiet docker.service || systemctl enable docker.service
