#!/usr/bin/env bash
#
# This script sets up the current environment to be able to build multi-arch Docker images, installing QEMU

set -e

# Set up QEMU
docker run --privileged --rm tonistiigi/binfmt --install amd64,arm64,arm

# Create a buildx builder with support for multi-arch
docker buildx create --use --name mybuilder
