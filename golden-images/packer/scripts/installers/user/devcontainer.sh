#!/bin/bash -e
################################################################################
##  File:  devcontainer.sh
##  Desc:  Configure DevContainer Specific things
################################################################################
echo "Running $0"

# Remove PyTorch and Reinstall with only CPU Support
# Note: we do this as the disk space is limited and we don't need GPU support for testing
# pip list | grep nvidia | awk '{print $1}' | xargs pip uninstall -y

# Install PyTorch CPU
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
