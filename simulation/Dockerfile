# Build stage
# FROM python:3.8 AS wheel_ale_py
FROM python:3.8

# Install dependencies for building ALE
RUN apt update && \
    apt install -y python3 python3-pip git cmake libsdl2-dev libboost-all-dev swig

# Set working directory
WORKDIR /app

# Copy the pyproject.toml files to the container
COPY pyproject.toml /app/

# Install dependencies
# virtualenvs.create false: don't create a virtualenv as we are in a virtual env (docker)
RUN pip install --upgrade pip \
    && pip install . \
    && pip install swig
#RUN poetry config virtualenvs.create false \
#    && poetry install --no-interaction --no-ansi --no-root

RUN ls -la /app
# Copy the rest of the project files to the container
COPY . /app

# Copy the docker script
COPY docker/docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Start the docker script
CMD ["docker-entrypoint.sh"]
