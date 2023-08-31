#!/bin/bash -e
################################################################################
##  File:  bashrc.sh
##  Desc:  Configure bashrc for on-boot behavior
################################################################################
# Enable MOTD
echo "run-parts /etc/update-motd.d" >> /home/${SSH_USER}/.zshrc
echo "run-parts /etc/update-motd.d" >> /home/${SSH_USER}/.bashrc

echo "cat /etc/update-motd.d/01-custom.txt" >> /home/${SSH_USER}/.zshrc
echo "cat /etc/update-motd.d/01-custom.txt" >> /home/${SSH_USER}/.bashrc

# Navigate to Default Directory
echo "cd /home/${SSH_USER}" >> /home/${SSH_USER}/.zshrc
echo "cd /home/${SSH_USER}" >> /home/${SSH_USER}/.bashrc

# Start Docker
echo "sudo service docker start" >> /home/${SSH_USER}/.zshrc
echo "sudo service docker start" >> /home/${SSH_USER}/.bashrc

# Init PyEnv
echo "source ~/.pyenvrc" >> /home/${SSH_USER}/.zshrc
echo "source ~/.pyenvrc" >> /home/${SSH_USER}/.bashrc
