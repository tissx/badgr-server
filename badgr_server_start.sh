#!/bin/bash

NAME="badgr-server"
USER=badgr
GROUP=www-data
WORKERS=3
BIND=127.0.0.1:9005
PID_DIR=/tmp/gunicorn.pid
#DJANGO_SETTINGS_MODULE=badgr-server.
DJANGO_WSGI_MODULE=wsgi
#LOG_LEVEL=error
DJANGODIR=/edx/app/badgr/badgr-server

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../badgr_env/bin/activate
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

#export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

exec ../badgr_env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $WORKERS \
--bind=$BIND \
--pid=$PID_DIR \
--log-level=$LOG_LEVEL  \
--log-file=-
#exec python badgr-server/manage.py runserver 127.0.0.1:9005
