#!/bin/bash -e
################################################################################
##  File:  bashrc.sh
##  Desc:  Configure bashrc for on-boot behavior
################################################################################
# Enable Custom MOTD
echo "cat /etc/update-motd.d/01-custom.txt" >> /home/${SSH_USER}/.zshrc
echo "cat /etc/update-motd.d/01-custom.txt" >> /home/${SSH_USER}/.bashrc

# Navigate to Default Directory
echo "cd /home/${SSH_USER}" >> /home/${SSH_USER}/.zshrc
echo "cd /home/${SSH_USER}" >> /home/${SSH_USER}/.bashrc

# # Start Docker
# echo "sudo service docker start" >> /home/${SSH_USER}/.zshrc
# echo "sudo service docker start" >> /home/${SSH_USER}/.bashrc
