#!/bin/bash
######################################################
# Composabl Sim Dockerfile - Version 1.0.0
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
IS_HISTORIAN_ENABLED=${IS_HISTORIAN_ENABLED:-"false"}
COMPOSBAL_VERSION=$(python -c "import importlib.metadata; print(importlib.metadata.version('composabl-core'))" > /dev/null 2>&1)

# Function to convert values to boolean
to_boolean() {
    local value="$1"
    if [[ "$value" == "true" || "$value" == "True" || "$value" == "1" ]]; then
        echo "true"
    else
        echo "false"
    fi
}

# Convert to boolean
IS_HISTORIAN_ENABLED=$(to_boolean "$IS_HISTORIAN_ENABLED")
IS_DEBUG=$(to_boolean "$IS_DEBUG")

# Generate SIM ID
SIM_ID=${SIM_ID:-"sim-$(uuidgen)"}
APP_NAME=$SIM_ID
STANDALONE_MQTT_CONSUMER_ID=$SIM_ID

# Print startup information
echo "- SIM_ID: $SIM_ID"
echo "- MODE: $MODE"
echo "- IS_HISTORIAN_ENABLED: $IS_HISTORIAN_ENABLED"
echo "- COMPOSABL_VERSION: $COMPOSBAL_VERSION"
echo "- APP_NAME: $APP_NAME"
echo "- APP_PATH: $APP_PATH"
echo '===================================================================='

if [[ "$IS_DEBUG" == "true" && "$MODE" == "standalone" ]]; then
    echo "- STANDALONE_MQTT_URL: $STANDALONE_MQTT_URL"
    echo "- STANDALONE_MQTT_CONSUMER_ID: $STANDALONE_MQTT_CONSUMER_ID"
    echo '===================================================================='
fi

# Navigate to the app directory
cd "$APP_PATH"

if [[ "$MODE" == "standalone" && "$IS_HISTORIAN_ENABLED" == "true" ]]; then
    echo "[Dapr] Running with Dapr in Standalone mode, configuring components..."

    # Patch /components/*yaml files with env variables
    for file in /docker/dapr/components/*.yaml; do
        echo "[Dapr] Patching $file with the env variables"

        cp "$file" "$file.bak"
        envsubst < "$file.bak" > "$file"
        rm "$file.bak"
    done

    echo '===================================================================='

    # Start the app with dapr
    echo "[Dapr] Starting $APP_NAME with Dapr"
    echo "[Dapr] - PATH: '$APP_PATH'"
    echo "[Dapr] - CMD: '$APP_CMD'"
    echo '===================================================================='

    dapr run --app-id "$SIM_ID" --app-port 50051 --dapr-http-port 3500 --app-protocol grpc \
        --resources-path /docker/dapr/components \
        -- \
        $APP_CMD
else
    echo "Starting $APP_NAME"
    echo '===================================================================='

    $APP_CMD
fi
