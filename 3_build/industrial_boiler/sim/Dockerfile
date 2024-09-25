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

# 2 option blocks below. You can choose one of them by commenting out the other.
# ==============================================================================
# 1. If you want to use the argument passed in the docker build command
# RUN sed -i "s/composabl.*/composabl==${COMPOSABL_VERSION}/g" requirements.txt \
#     && pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt

# 2. If you want to use the latest version of composabl
RUN pip install --no-cache-dir --upgrade pip \
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

EXPOSE 1337

CMD ["composabl-sim-entrypoint.sh"]
