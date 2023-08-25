#!/bin/bash
PATH_ROOT=$(readlink -f $(dirname $0))

# Ensure emqx has been started locally in docker, else install it and get the host name and user pass

# Dashboard: http://localhost:18083 (user: admin, pass: public)
# Ports: 1883 = TCP MQTT Port | 8081 = HTTP API | 8083 = MQTT/SSL Port | 8883 = MQTT/Websocket/SSL Port | 8084 = MQTT/Websocket Port | 18083 = Dashboard
echo "Starting MQTT Broker"

if docker ps | grep -q emqx; then
    echo "Emqx is already running"
else
    echo "Starting EMQX"
    docker run -d --rm --name emqx \
        -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 \
        -e EMQX_DASHBOARD__DEFAULT_USERNAME=admin \
        -e EMQX_DASHBOARD__DEFAULT_PASSWORD=admin \
        emqx/emqx
fi

echo "Starting App"
APP_ID=${COMPOSABL_APP_ID:-"gymnasiumsim"}
cd $PATH_ROOT/..
dapr run \
    --app-id=$APP_ID \
    --components-path=$PATH_ROOT/components \
    --dapr-http-port=3500 \
    -- $PATH_ROOT/../docker/docker-entrypoint.sh
