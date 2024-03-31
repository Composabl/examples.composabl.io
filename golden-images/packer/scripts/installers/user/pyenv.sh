#!/bin/bash -e
################################################################################
##  File:  pyenv.sh
##  Desc:  Installs Python via pyenv
##  Ref: https://github.com/actions/runner-images/blob/71e9516cb7fc9345b5e1787d44557fde50c128f4/images/linux/scripts/installers/python.sh
################################################################################
VERSION_PYTHON=${VERSION_PYTHON:-"3.11.8"}

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
export PYENV_ROOT=/home/${SSH_USER}/.pyenv

curl https://pyenv.run | bash

# Add pyenv to PATH and declare the PYENV_ROOT variable
setEtcEnvironmentVariable "PYENV_ROOT" $PYENV_ROOT
prependEtcEnvironmentPath "$PYENV_ROOT/bin:$PYENV_ROOT/shims"
reloadEtcEnvironment

# Configure the shell environment
cat << 'EOF' > "$HOME"/.pyenvrc
export PATH="$HOME"/.pyenv/bin:"$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF

cat << EOF >> "$HOME"/.bash_profile
if [ -f ~/.pyenvrc ]; then
        . ~/.pyenvrc
fi
EOF

# Install Python versions
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install $VERSION_PYTHON
pyenv global $VERSION_PYTHON

# Upgrade pip
pip install --upgrade pip
