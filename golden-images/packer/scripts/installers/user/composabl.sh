#!/bin/bash -e
################################################################################
##  File:  composabl.sh
##  Desc:  Configure Composabl Specific things (e.g., install libs, examples, ...)
################################################################################
# Install PyTorch CPU already
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install the composabl package
pip install --upgrade composabl==$VERSION_COMPOSABL

# Install the composabl examples repo
git clone https://github.com/Composabl/examples.composabl.io.git /home/${SSH_USER}/examples.composabl.io

# Remove PyTorch and Reinstall with only CPU Support
# Note: we do this as the disk space is limited and we don't need GPU support for testing
# pip uninstall torch torchvision torchaudio -y
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip list | grep nvidia | awk '{print $1}' | xargs pip uninstall -y
