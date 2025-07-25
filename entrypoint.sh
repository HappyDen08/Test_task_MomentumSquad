#!/bin/sh
set -e

echo "Запуск міграцій..."
python manage.py migrate

echo "Збірка статики..."
python manage.py collectstatic --noinput

echo "Підрахунок користувачів..."
USER_COUNT=$(python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Test_task_MomentumSquad.settings'); django.setup(); from django.contrib.auth import get_user_model; print(get_user_model().objects.count())" | tr -d '\r\n ')

echo "USER_COUNT=$USER_COUNT"

if [ "$USER_COUNT" = "0" ]; then
  echo "Користувачі відсутні. Завантажуємо фікстуру test_data.json ..."
  python manage.py loaddata test_data.json
else
  echo "Користувачі вже є. Пропускаємо завантаження фікстури."
fi

echo "Запуск сервера..."
exec gunicorn Test_task_MomentumSquad.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --preload
