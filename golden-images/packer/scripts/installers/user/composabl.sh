#!/bin/bash -e
################################################################################
##  File:  composabl.sh
##  Desc:  Configure Composabl Specific things (e.g., install libs, examples, ...)
################################################################################
echo $VERSION_COMPOSABL
printenv

# Install the composabl package
pip install --upgrade composabl==${VERSION_COMPOSABL}

# Install the composabl examples repo
git clone https://github.com/Composabl/examples.composabl.io.git /home/${SSH_USER}/examples.composabl.io
