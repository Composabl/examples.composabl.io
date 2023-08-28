#!/bin/bash -e
################################################################################
##  File:  wsl.sh
##  Desc:  Configure Linux for WSL Specific Usage
################################################################################
echo "[user]\ndefault=${SSH_USER}" >> /etc/wsl.conf
