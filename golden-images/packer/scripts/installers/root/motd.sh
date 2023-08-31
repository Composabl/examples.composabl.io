#!/bin/bash -e
################################################################################
##  File:  motd.sh
##  Desc:  Sets the message of the day with an EOF
################################################################################

# Note: we use 'EOF' as single quotes mean literal text
cat << 'EOF' > /etc/update-motd.d/01-custom.txt
====================================================================
          ____                                      _     _
         / ___|___  _ __ ___  _ __   ___  ___  __ _| |__ | |
        | |   / _ \| '_ ` _ \| '_ \ / _ \/ __|/ _` | '_ \| |
        | |__| (_) | | | | | | |_) | (_) \__ \ (_| | |_) | |
         \____\___/|_| |_| |_| .__/ \___/|___/\__,_|_.__/|_|
                             |_|
====================================================================

👋 Welcome to the Composabl dev container! You are on our Demo image.
It includes everything to provide demonstrations around the Composabl SDK.

🎓 If you are looking to run the Composabl quickstarts and tutorials, head over to
https://github.com/Composabl/examples.composabl.io instead.

📚 If you are looking for the Composabl documentation, head over to https://docs.composabl.io.

🐍 Python is configured through PyEnv, simply run 'pyenv versions' to see the installed versions and
switch between them with 'pyenv global <version>'.
EOF

# Make the printer
cat << 'EOF' > /etc/update-motd.d/01-custom.sh
cat /etc/update-motd.d/01-custom.txt
EOF

sudo chmod +x /etc/update-motd.d/01-custom.sh

# Ensure the motd is ran on startup through bashrc and zshrc
echo "run-parts /etc/update-motd.d" >> /home/${SSH_USER}/.bashrc
echo "run-parts /etc/update-motd.d" >> /home/${SSH_USER}/.zshrc
