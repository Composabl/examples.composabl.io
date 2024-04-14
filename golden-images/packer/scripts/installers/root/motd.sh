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

👋 Welcome to the Composabl Dev Image!
It includes everything to provide demonstrations around the Composabl SDK.

🔑 Request a License at https://forms.microsoft.com/r/SLFGXm1Ggp and configure it with
`export COMPOSABL_LICENSE="YOUR_KEY"`.

Next things to do:
- 📄 Approve the EULA: `export COMPOSABL_EULA_AGREED=1`
- 📚 Read Documentation: https://docs.composabl.com.
- 🎓 Explore Quickstarts: https://github.com/Composabl/examples.composabl.io
- 🚀 Run your first Agent: `cd agents/cstr/deep_reinforcement_learning/; python agent.py`

EOF

# Make the printer
cat << 'EOF' > /etc/update-motd.d/01-custom.sh
cat /etc/update-motd.d/01-custom.txt
EOF

chmod +x /etc/update-motd.d/01-custom.sh

# Ensure the motd is ran on startup through bashrc and zshrc
echo "run-parts /etc/update-motd.d" >> /home/${SSH_USER}/.bashrc
echo "run-parts /etc/update-motd.d" >> /home/${SSH_USER}/.zshrc
