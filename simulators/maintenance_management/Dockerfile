######################################################
# Composabl Sim Dockerfile - Version 1.0.0
######################################################
# Build stage
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies for protobuf
RUN apt-get update \
    && apt-get install --yes protobuf-compiler wget curl gettext-base uuid-runtime

######################################################
# Install Dapr
# note: this adds 258MB to the image size
######################################################
# Install dapr CLI
RUN wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash

# Install daprd to /opt/dapr
# ARG DAPR_BUILD_DIR
# COPY $DAPR_BUILD_DIR /opt/dapr
# ENV PATH="/opt/dapr/:${PATH}"
RUN dapr init --slim

######################################################
# Install Python Dependencies
######################################################
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

######################################################
# Install App Code
######################################################
# Copy over the scripts
COPY docker /docker

# Copy the application code
COPY . .

######################################################
# Run
######################################################
COPY docker/entrypoint.sh /usr/local/bin/composabl-sim-entrypoint.sh
RUN chmod +x /usr/local/bin/composabl-sim-entrypoint.sh

CMD ["composabl-sim-entrypoint.sh"]
