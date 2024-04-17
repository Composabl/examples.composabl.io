######################################################
# Composabl Sim Dockerfile - Version 2.0.0
#
# CHANGELOG
# Version 2.0.0:
#   - Update to Python 3.11
#   - Dynamic composabl-version from Dockerfile args
# Version 1.0.0:
#   - Initial build file
######################################################
# Build stage
# FROM python:3.8-slim
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for protobuf
RUN apt-get update \
    && apt-get install --yes protobuf-compiler wget curl gettext-base uuid-runtime \
    build-essential g++ swig

######################################################
# Install Python Dependencies
######################################################
ARG COMPOSABL_VERSION

COPY requirements.txt ./
RUN sed -i "s/composabl-core.*/composabl-core==${COMPOSABL_VERSION}/g" requirements.txt \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

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
