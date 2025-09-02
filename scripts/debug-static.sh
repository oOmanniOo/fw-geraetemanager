#!/bin/bash

echo "🔍 Debugging statische Dateien..."

# Prüfe ob Container läuft
echo "📊 Container Status:"
docker-compose -f docker-compose.prod-simple.yml ps

echo ""
echo "📁 Statische Dateien im Container:"
docker-compose -f docker-compose.prod-simple.yml exec web ls -la /app/staticfiles/

echo ""
echo "📁 Django Admin statische Dateien:"
docker-compose -f docker-compose.prod-simple.yml exec web find /app/staticfiles/admin -name "*.css" | head -5

echo ""
echo "🔧 Django Settings prüfen:"
docker-compose -f docker-compose.prod-simple.yml exec web python manage.py shell -c "
from django.conf import settings
print(f'STATIC_URL: {settings.STATIC_URL}')
print(f'STATIC_ROOT: {settings.STATIC_ROOT}')
print(f'STATICFILES_DIRS: {settings.STATICFILES_DIRS}')
print(f'DEBUG: {settings.DEBUG}')
"

echo ""
echo "📋 Collectstatic erneut ausführen:"
docker-compose -f docker-compose.prod-simple.yml exec web python manage.py collectstatic --noinput --verbosity=2

echo ""
echo "✅ Debug abgeschlossen!"
