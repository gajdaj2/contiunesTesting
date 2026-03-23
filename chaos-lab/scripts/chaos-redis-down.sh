#!/bin/bash

echo "💣 CHAOS: Wyłączanie Redis..."
docker compose stop redis

echo "⏸️  Redis jest wyłączony"
echo "🔍 Obserwuj odpowiedź aplikacji:"
echo ""
echo "Przejdź na: curl http://localhost:3000/users/cached"
echo "Powinno pobierać z bazy zamiast z cache'u"
echo "Metryki: curl http://localhost:3000/metrics | grep cache"
echo ""
echo "Naciśnij Enter, aby włączyć Redis..."
read

echo "🔄 Włączanie Redis..."
docker compose start redis

echo "✅ Redis włączony"