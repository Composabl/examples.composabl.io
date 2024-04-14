#!/bin/bash
echo "Container started, executing entrypoint commands..."

# Execute the command specified as CMD in Dockerfile, or any command passed to docker run
exec "$@"
