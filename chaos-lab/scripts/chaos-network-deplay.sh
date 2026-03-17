#!/bin/bash

CONTAINER="chaos-app"
DELAY="${1:-500}ms"  # Domyślnie 500ms

echo "💣 CHAOS: Dodawanie opóźnienia sieciowego ($DELAY)..."

docker exec $CONTAINER sh -c \
  "tc qdisc add dev eth0 root netem delay $DELAY"

echo "⏸️  Opóźnienie sieciowe dodane"
echo "Testuj: curl -w 'Response time: %{time_total}s\n' http://localhost:3000/health"
echo ""
echo "Naciśnij Enter, aby usunąć opóźnienie..."
read

echo "🔄 Usuwanie opóźnienia..."
docker exec $CONTAINER sh -c "tc qdisc del dev eth0 root netem"

echo "✅ Opóźnienie usunięte"