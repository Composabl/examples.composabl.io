#!/bin/bash -e
################################################################################
##  File:  wsl.sh
##  Desc:  Configure Linux for WSL Specific Usage
################################################################################
# Configure WSL to do the following:
# 1. Enable metadata and disable case sensitivity for NTFS mounts
# 2. Enable interop between WSL and Windows
# 3. Enable DNS resolution
# 4. Enable user to run sudo without password
# 5. Enable default user to be the ${SSH_USER}
cat << EOF > /etc/wsl.conf
[automount]
enabled = true
options = "metadata,uid=1000,gid=1000,umask=0022,fmask=11,case=off"
mountFsTab = false
crossDistro = true

[filesystem]
umask = 0022

[network]
generateHosts = true
generateResolvConf = true

[interop]
enabled = true

[user]
default = ${SSH_USER}
EOF
