#!/bin/bash
V_COMPOSABL_SIM=${V_COMPOSABL_SIM:-"1.1.0"}

######################################################
# Composabl Sim Entrypoint - Version 1.1.0
######################################################

echo '===================================================================='
echo '          ____                                      _     _         '
echo '         / ___|___  _ __ ___  _ __   ___  ___  __ _| |__ | |        '
echo '        | |   / _ \| '\''_  '\''_ \| '\''_ \ / _ \/ __|/ _` |'\''_ '\''\| |        '
echo '        | |__| (_) | | | | | | |_) | (_) \__ \ (_| | |_) | |        '
echo '         \____\___/|_| |_| |_| .__/ \___/|___/\__,_|_.__/|_|        '
echo '                             |_|                                    '
echo '===================================================================='

# Default values
APP_CMD=${APP_CMD:-"python src/main.py"}
APP_PATH=${APP_PATH:-"/app"}
IS_DEBUG=${IS_DEBUG:-false}
MODE=${MODE:-standalone}  # kubernetes | standalone
COMPOSABL_VERSION=$(python -c "import importlib.metadata; print(importlib.metadata.version('composabl-core'))" > /dev/null 2>&1)
HISTORIAN_MONIKER_MQTT=${HISTORIAN_MONIKER_MQTT:-"tcp://mqtt:1883"}

# Function definitions
to_boolean() {
    local value="$1"
    if [[ "$value" == "true" || "$value" == "True" || "$value" == "1" ]]; then
        echo "true"
    else
        echo "false"
    fi
}

is_set() {
    local value="$1"
    if [[ -z "$value" ]]; then
        echo "false"
    else
        echo "true"
    fi
}

# Convert to boolean
IS_DEBUG=$(to_boolean "$IS_DEBUG")
IS_HISTORIAN_ENABLED=$(is_set "$HISTORIAN_MONIKER_MQTT")

# Generate SIM ID
SIM_ID=${SIM_ID:-"sim-$(uuidgen)"}
APP_NAME=$SIM_ID
HISTORIAN_MONIKER_MQTT_CONSUMER_ID=$SIM_ID

# Print startup information
echo "- SIM_ID: $SIM_ID"
echo "- MODE: $MODE"
echo "- IS_HISTORIAN_ENABLED: $IS_HISTORIAN_ENABLED"
echo "- V_COMPOSABL_CORE: $(pip show "composabl-core-dev" | grep '^Version:' | awk '{print $2}')"
echo "- V_COMPOSABL_SIM: $V_COMPOSABL_SIM"
echo "- APP_NAME: $APP_NAME"
echo "- APP_PATH: $APP_PATH"
echo '===================================================================='

if [[ "$IS_DEBUG" == "true" && "$MODE" == "standalone" ]]; then
    echo "- HISTORIAN_MONIKER_MQTT: $HISTORIAN_MONIKER_MQTT"
    echo "- HISTORIAN_MONIKER_MQTT_CONSUMER_ID: $HISTORIAN_MONIKER_MQTT_CONSUMER_ID"
    echo '===================================================================='
fi

# Navigate to the app directory
cd "$APP_PATH"

echo "Starting $APP_NAME"
echo '===================================================================='

$APP_CMD --host $HOST --port $PORT
