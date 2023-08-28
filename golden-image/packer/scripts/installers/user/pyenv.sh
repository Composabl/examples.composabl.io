#!/bin/bash -e
################################################################################
##  File:  pyenv.sh
##  Desc:  Installs Python 2/3
##  Ref: https://github.com/actions/runner-images/blob/71e9516cb7fc9345b5e1787d44557fde50c128f4/images/linux/scripts/installers/python.sh
################################################################################
VERSION_PYTHON=${VERSION_PYTHON:-"3.8.17"}

# Source the helpers for use with the script
source $HELPER_SCRIPTS/etc-environment.sh
source $HELPER_SCRIPTS/os.sh

# Require packages
# TODO: tzdata is installed as part of this, which is blocking the installation, figure out why
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev

# Install PyEnv to /home/$SSH_USER/.pyenv
# https://github.com/pyenv/pyenv-installer/blob/master/bin/pyenv-installer
# export PYENV_ROOT=/home/${SSH_USER}/.pyenv
curl https://pyenv.run | bash

# Add pyenv to PATH and declare the PYENV_ROOT variable
setEtcEnvironmentVariable "PYENV_ROOT" $PYENV_ROOT
prependEtcEnvironmentPath '$PYENV_ROOT/bin:$PYENV_ROOT/shims'
reloadEtcEnvironment

# Add eval "$(pyenv init -)" to shell profile
# so that pyenv will be loaded automatically
echo 'eval "$(pyenv init -)"' | tee -a /etc/profile.d/pyenv.sh

# Reload the shell
source /etc/profile.d/pyenv.sh

# # Load PyEnv (from absolute path)
# # this way we can initialize it
# export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
# eval "$(pyenv init -)"

# Install Python versions
pyenv install $VERSION_PYTHON
pyenv global $VERSION_PYTHON
