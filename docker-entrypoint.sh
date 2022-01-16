#!/bin/sh
python ./source/manage.py migrate --noinput
SOCKET_LISTEN_QUEUE_SIZE=${SOCKET_LISTEN_QUEUE_SIZE-128}

uwsgi --ini ./source/Loyalty_Program_App/wsgi/uwsgi.ini

exec "$@"
