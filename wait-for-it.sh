#!/bin/sh

set -e

host="$DB_HOST"
port="$DB_PORT"

echo "Waiting for MariaDB at $host:$port..."

while ! nc -z $host $port; do
  sleep 1
done

echo "MariaDB is up – executing command"
exec "$@"
