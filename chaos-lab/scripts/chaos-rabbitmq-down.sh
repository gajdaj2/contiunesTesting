#!/bin/bash

echo "💣 CHAOS: Wyłączanie RabbitMQ..."
docker-compose stop rabbitmq

echo "⏸️  RabbitMQ jest wyłączony"
echo "🔍 Obserwuj odpowiedź aplikacji:"
echo ""
echo "Testuj queue: curl -X POST http://localhost:3000/jobs"
echo "Powinno zwrócić 503 Service Unavailable"
echo ""
echo "Naciśnij Enter, aby włączyć RabbitMQ..."
read

echo "🔄 Włączanie RabbitMQ..."
docker-compose start rabbitmq

echo "✅ RabbitMQ włączony"