#!/bin/sh
clear
source collect_env/bin/activate
cd collect/
python3 manage.py makemigrations
python3 manage.py migrate
if [ "$1" = "docker" ]
    then
    echo "Running Server on Docker"
    chromium-browser&
    python3 manage.py runserver 172.17.0.2:8000
else
    echo "Running Server on Local"
    python3 manage.py runserver 0.0.0.0:8000
fi