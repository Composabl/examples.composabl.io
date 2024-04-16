#!/bin/bash -e
################################################################################
##  File:  apt.sh
##  Desc:  Update apt and install base packages
################################################################################
apt-get update

# tzdata is annoying as it requires user input, configure a timezone for the user
TZ=America/Los_Angeles
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install base packages
apt-get install -y apt-transport-https ca-certificates curl software-properties-common git curl sudo jq tzdata vim nano wget \
    libpq-dev # Required for psycopg2
