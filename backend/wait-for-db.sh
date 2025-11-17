
set -e

host="$DB_HOST" # PostgreSQL host
port="$DB_PORT" # PostgreSQL port

echo "Waiting for PostgreSQL at $host:$port..." #waiting for postgres

until nc -z $host $port; do #wait until postgres is available
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing command" #when postgres is available, execute the command passed as arguments
exec "$@"
