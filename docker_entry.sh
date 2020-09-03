#!/bin/sh

if [ "x$SQL_HOST" != "x" ] && [ "x$SQL_PORT" != "x" ]; then
  echo "Waiting for db..."

  while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
    sleep 0.1
  done

  echo "db started"
fi

[ "x$SQL_DO_FLUSH" = "x1" ] && python manage.py flush --no-input
python manage.py migrate

exec "$@"
