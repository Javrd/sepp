#!/bin/bash
cd /var/www/html/aib
python manage.py collectstatic --noinput
echo "Waiting for mysql"
while ! mysqladmin ping -h"$MYSQL_HOST" --silent; do
  printf "."
  sleep 1
done

echo -e "\nmysql ready"
python manage.py migrate
python populate.py
daphne -b 0.0.0.0 -p 80 artinbar.asgi:application