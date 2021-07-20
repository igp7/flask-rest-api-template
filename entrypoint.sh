#!/bin/sh

if [[ -z "${APP_ENV}" ]]; then
  source .env.pro;
fi

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $BBDD_HOST $BBDD_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

if [ "$APP_ENV" = "local" ]; then
  flask create-db
  flask create-user-admin
  gunicorn --bind $API_HOST:$API_PORT $API_ENTRYPOINT;
fi

if [ "$APP_ENV" = "production" ]; then
  if [ "$PLATFORM_DEPLOY" = "heroku" ]; then
    gunicorn --bind $API_HOST:$PORT $API_ENTRYPOINT;
  else
    gunicorn --bind $API_HOST:$API_PORT $API_ENTRYPOINT;
  fi
fi