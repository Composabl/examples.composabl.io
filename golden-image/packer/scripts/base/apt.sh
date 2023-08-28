#!/bin/bash -e
################################################################################
##  File:  apt.sh
##  Desc:  Update apt and install base packages
################################################################################
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common git curl sudo jq
apt-get -yq dist-upgrade
