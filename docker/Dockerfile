# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT=3.8
FROM python:${VARIANT}-bullseye

# [Option] Install zsh
ARG INSTALL_ZSH="true"

# [Options] Versions
ARG KUBECTL_VERSION="latest"
ARG HELM_VERSION="latest"
ARG MINIKUBE_VERSION="latest"

# This Dockerfile adds a non-root 'composabl' user with sudo access. However, for Linux,
# this user's GID/UID must match your local user UID/GID to avoid permission issues
# with bind mounts. Update USER_UID / USER_GID if yours is not 1000. See
# https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=composabl
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Setup default python tools in a venv via pipx to avoid conflicts
ENV PIPX_HOME=/usr/local/py-utils \
    PIPX_BIN_DIR=/usr/local/py-utils/bin

ENV PATH=${PATH}:${PIPX_BIN_DIR}

# Setup image using library scripts and configure non-root user.
COPY library-scripts/* custom-scripts/* first-run-notice.txt /tmp/staging/

RUN apt-get update \
    #
    && echo "Configuring noninteractive mode" \
    && export DEBIAN_FRONTEND=noninteractive \
    #
    && echo "Installing needed packages and setup the environment and non-root user" \
    && bash /tmp/staging/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "true" "true" "true" \
    #
    && echo "Adding additional custom configurations for non-root user" \
    && bash /tmp/staging/setup-user.sh "${USERNAME}" "${PATH}" \
    #
    && echo "Installing the Docker CLI and Engine for Docker-in-Docker (using Docker CE)" \
    && bash /tmp/staging/docker-in-docker-debian.sh "true" "${USERNAME}" "false" "latest" \
    #
    && echo "Installing Kubectl, Helm and Minikube" \
    && bash /tmp/staging/kubectl-helm-debian.sh "${KUBECTL_VERSION}" "${HELM_VERSION}" "${MINIKUBE_VERSION}" \
    #
    && echo "Installing Python Tools" \
    && bash /tmp/staging/python-debian.sh "none" "/usr/local" "${PIPX_HOME}" "${USERNAME}" \
    #
    # Copy our init scripts to /usr/local/share.
    && mv -f -t /usr/local/share/ /tmp/staging/docker-bind-mount.sh /tmp/staging/devcontainer-init.sh /tmp/staging/setup-docker-multiarch.sh \
    && chmod +x /usr/local/share/docker-bind-mount.sh /usr/local/share/devcontainer-init.sh  /usr/local/share/setup-docker-multiarch.sh \
    && chown ${USERNAME}:root /usr/local/share/docker-bind-mount.sh /usr/local/share/devcontainer-init.sh  /usr/local/share/setup-docker-multiarch.sh \
    #
    # Move the first run notice to the correct location for Codespaces.
    && mkdir -p /usr/local/etc/vscode-dev-containers/ \
    && mv -f /tmp/staging/first-run-notice.txt /usr/local/etc/vscode-dev-containers/ \
    #
    # Set permissions for the workspace folder
    && mkdir -p /workspaces && chown ${USERNAME} /workspaces \
    #
    # Clean up packages and the staging folder.
    && apt-get autoremove -y && apt-get clean -y && rm -rf /tmp/staging

# Remove library scripts for final image
RUN rm -rf /tmp/library-scripts

# Mount for docker-in-docker
VOLUME [ "/var/lib/docker" ]

# Initialize Dapr devcontainer script
ENTRYPOINT [ "/usr/local/share/devcontainer-init.sh" ]
CMD [ "sleep", "infinity" ]

USER ${USERNAME}
