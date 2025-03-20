#!/bin/sh

echo "Waiting for PostgreSQL to be available..."
# Wait until PostgreSQL is ready; adjust the host, user, and database as needed.
until pg_isready -h db -U "$POSTGRES_USER" -d postgres; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done
echo "PostgreSQL is up - continuing."

echo "Applying database migrations..."
python manage.py migrate --noinput

#######################################
# Create superuser if not exists.
#######################################
create_or_check_superuser() {
  python manage.py createsuperuser --noinput \
                                   --username "$DJANGO_SUPERUSER_USERNAME" \
                                   --email "$DJANGO_SUPERUSER_EMAIL" 2>/dev/null
  [ $? -ne 0 ] && echo "Superuser already exists."
}
create_or_check_superuser

#######################################
# Check and create database if needed (optional)
#######################################
exec_postgres() {
  PGPASSWORD=$POSTGRES_PASSWORD psql -h db \
                                     -U $POSTGRES_USER \
                                     -d postgres \
                                     -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'"
}

create_database() {
  COMMAND="CREATE DATABASE $POSTGRES_DB"
  exec_postgres db postgres "$COMMAND"
}

check_database() {
  COMMAND="SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'"
  exec_postgres db postgres "$COMMAND" | grep -q 1
}

if [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ]; then
  echo "Failed. POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD must be set."
  exit 1
fi

echo "Checking if database $POSTGRES_DB exists..."
check_database
if [ $? -eq 0 ]; then
  echo "Database $POSTGRES_DB already exists."
else
  echo "Database $POSTGRES_DB does not exist. Creating..."
  create_database
  if [ $? -eq 0 ]; then
    echo "Database $POSTGRES_DB created successfully."
  else
    echo "Failed to create database $POSTGRES_DB."
    exit 1
  fi
fi

Xvfb :99 -screen 0 1024x768x16 &  # Start X virtual framebuffer
exec "$@"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn main_module.wsgi:application --bind 0.0.0.0:8000
