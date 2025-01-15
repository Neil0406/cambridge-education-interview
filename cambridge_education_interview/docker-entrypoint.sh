#!/bin/sh
#等待 MySQL 完成啟動
apt-get install netcat -y
echo "Waiting for MySQL to be ready..."
until nc -zv "$DB_HOST" "$DB_PORT"; do
    echo "MySQL is not ready yet, waiting..."
    sleep 2
done
echo "MySQL is up and running!"

pip install -r requirements.txt
python manage.py migrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python3 manage.py createsuperuser \
    --name "$DJANGO_SUPERUSER_USERNAME" \
    --phone "$DJANGO_SUPERUSER_PHONE" \
    --noinput || echo "Superuser already exists."
uwsgi --ini uwsgi.ini