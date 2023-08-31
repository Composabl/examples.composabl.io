#!/bin/bash -e
################################################################################
##  File:  python-packages.sh
##  Desc:  Install default python packages
################################################################################
# Load PyEnv (from absolute path)
# this way we can initialize it
export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
eval "$(pyenv init -)"

# Print Versions

pyenv --version
python --version
pip --version

pip install --upgrade pip
pip install --upgrade composabl
