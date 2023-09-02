#!/bin/bash -e
################################################################################
##  File:  poetry.sh
##  Desc:  Install Poetry
################################################################################
# Source the helpers for use with the script
source $HELPER_SCRIPTS/etc-environment.sh

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to path
prependEtcEnvironmentPath "$HOME/.local/bin"
