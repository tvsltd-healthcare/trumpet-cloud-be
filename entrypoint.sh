#!/bin/sh
set -e

# Check if the DATABASE environment variable is set
if [ "$DB_NAME" = "cloud-postgres" ]; then
    echo "Waiting for Trumpet Cloud server postgres..."

    # Wait for the database to be ready
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "Trumpet Cloud postgres server started!"
fi

python generate_tables.py
sleep 0.1
python main.py

exec "$@"
