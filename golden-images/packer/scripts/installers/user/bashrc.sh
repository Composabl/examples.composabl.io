#!/bin/bash -e
################################################################################
##  File:  bashrc.sh
##  Desc:  Configure bashrc for on-boot behavior
################################################################################
echo "Running bashrc.sh"

cat << EOF >> /home/${SSH_USER}/.basrc
# Enable Custom MOTD
cat /etc/update-motd.d/01-custom.txt

# Navigate to Default Directory
cd /home/${SSH_USER}/examples.composabl.io

# Accept the EULA
echo "Accepting the EULA automatically for you..."
echo "note: you can always unset this variable with 'unset COMPOSABL_EULA_AGREED'"
export COMPOSABL_EULA_AGREED=1

# Start Docker
sudo service docker start

# Ensure the bin location is added to the PATH
export PATH="$PATH:/home/${SSH_USER}/.local/bin"
EOF

cat << EOF >> /home/${SSH_USER}/.zshrc
# Enable Custom MOTD
cat /etc/update-motd.d/01-custom.txt

# Navigate to Default Directory
cd /home/${SSH_USER}/examples.composabl.io

# Accept the EULA
echo "Accepting the EULA automatically for you..."
echo "note: you can always unset this variable with 'unset COMPOSABL_EULA_AGREED'"
export COMPOSABL_EULA_AGREED=1

# Start Docker
sudo service docker start

# Ensure the bin location is added to the PATH
export PATH="$PATH:/home/${SSH_USER}/.local/bin"
EOF


# # Start Docker
# echo "sudo service docker start" >> /home/${SSH_USER}/.zshrc
# echo "sudo service docker start" >> /home/${SSH_USER}/.bashrc
