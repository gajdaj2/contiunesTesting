#!/bin/bash

API="http://localhost:3000"

clear
echo "================================"
echo "📊 MONITORING CHAOS LAB"
echo "================================"
echo ""

while true; do
  clear
  echo "================================"
  echo "📊 MONITORING - $(date +'%H:%M:%S')"
  echo "================================"
  echo ""

  # Health status
  echo "🏥 STATUS ZDROWOTNOŚCI:"
  HEALTH=$(curl -s $API/health)
  echo "$HEALTH" | jq '.services' 2>/dev/null || echo "❌ Aplikacja niedostępna"
  echo ""

  # Kontener stats
  echo "📈 STATYSTYKI KONTENERÓW:"
  docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null | head -5
  echo ""

  # Liczniki
  echo "📊 METRYKI:"
  curl -s $API/metrics 2>/dev/null | grep -E "^(cache|db_query|http_request)" | head -10 || echo "Brak metryk"
  echo ""

  echo "Odśwież za 5 sekund... (Ctrl+C aby zatrzymać)"
  sleep 5
done