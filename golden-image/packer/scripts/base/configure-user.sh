#!/bin/bash -e
################################################################################
##  File:  configure-user.sh
##  Desc:  Add user and configure it to the sudoers
################################################################################
echo "Configuring user: ${SSH_USER}"

useradd -m ${SSH_USER}
echo "${SSH_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Print active user
echo "Active user: $(whoami)"
