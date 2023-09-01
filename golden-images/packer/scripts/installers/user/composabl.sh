#!/bin/bash -e
################################################################################
##  File:  composabl.sh
##  Desc:  Configure Composabl Specific things (e.g., install libs, examples, ...)
################################################################################
# Load PyEnv (from absolute path)
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
eval "$(pyenv init -)"

# Install the composabl prod library
# note: this will inflate the image by a lot as it installs Ray, Torch and CUDA dependencies
pip install --upgrade pip
pip install --upgrade composabl

# Install the composabl examples repo
git clone https://github.com/Composabl/examples.composabl.io.git
