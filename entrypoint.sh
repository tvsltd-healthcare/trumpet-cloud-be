#!/bin/sh
set -e

# Check if the DATABASE environment variable is set
if [ "$DATABASE" = "trumpet-node-dashboard" ]; then
    echo "Waiting for Trumpet's dashboard postgres..."

    # Wait for the database to be ready
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "Trumpet's dashboard postgres started!"
fi

# Start the Gunicorn server
exec gunicorn app_layer_entrypoint:app \
    --bind 0.0.0.0:8080 \
    --log-level info \
    --timeout 180 \
    --workers 3 \
    --worker-class uvicorn.workers.UvicornWorker "$@"
