#!/bin/bash -e
################################################################################
##  File:  devcontainer.sh
##  Desc:  Configure DevContainer Specific things
################################################################################
echo "Running devcontainer.sh"

# Install PyTorch CPU
pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cpu
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
