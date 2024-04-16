#!/bin/bash -e
################################################################################
##  File:  composabl.sh
##  Desc:  Configure Composabl Specific things (e.g., install libs, examples, ...)
################################################################################
echo "Running composabl.sh"

# Install the composabl package
pip install composabl==${VERSION_PIP_COMPOSABL}

# Install extra packages
pip install psycopg2   # Required for the PostgresSQL example
pip install ipywidgets # Required for the Jupyter Notebook

# Remove PyTorch and Reinstall with only CPU Support
# Note: we do this as the disk space is limited and we don't need GPU support for testing
# pip list | grep nvidia | awk '{print $1}' | xargs pip uninstall -y

# Install the composabl examples repo
git clone https://github.com/Composabl/examples.composabl.io.git /home/${SSH_USER}/examples.composabl.io
