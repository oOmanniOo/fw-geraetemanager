#!/bin/bash

echo "🔍 Debugging Nginx..."

# Nginx-Konfiguration testen
echo "📋 Nginx-Konfiguration testen:"
docker-compose -f docker-compose.prod.yml exec nginx nginx -t

echo ""
echo "📁 Statische Dateien in Nginx-Container:"
docker-compose -f docker-compose.prod.yml exec nginx ls -la /app/staticfiles/

echo ""
echo "🌐 Nginx-Logs:"
docker-compose -f docker-compose.prod.yml logs nginx --tail=20

echo ""
echo "🔧 Nginx-Prozess:"
docker-compose -f docker-compose.prod.yml exec nginx ps aux

echo ""
echo "✅ Nginx-Debug abgeschlossen!"
