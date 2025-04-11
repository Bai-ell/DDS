#!/bin/bash
set -e

echo "⏳ Ждём базу..."
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "База недоступна — ждём..."
  sleep 1
done
echo "✅ База готова!"

echo "🛠️  Миграции..."
python manage.py migrate --noinput

echo "📦 Собираем статику..."
python manage.py collectstatic --noinput

if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  echo "🔐 Создаём суперпользователя..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        '$DJANGO_SUPERUSER_USERNAME',
        '$DJANGO_SUPERUSER_EMAIL',
        '$DJANGO_SUPERUSER_PASSWORD'
    )
"
fi

echo "🚀 Запускаем: $@"
exec "$@"
