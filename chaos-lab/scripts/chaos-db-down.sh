#!/bin/bash

echo "💣 CHAOS: Wyłączanie PostgreSQL..."
docker compose pause postgres

echo "⏸️  PostgreSQL jest wstrzymany"
echo "🔍 Obserwuj odpowiedź aplikacji:"
echo ""
echo "Sprawdzaj zdrowotność: curl http://localhost:3000/health"
echo "Testuj dostęp do DB: curl http://localhost:3000/users/db"
echo "Testuj cache: curl http://localhost:3000/users/cached"
echo ""
echo "Naciśnij Enter, aby wznowić PostgreSQL..."
read

echo "🔄 Wznowienie PostgreSQL..."
docker compose unpause postgres

echo "✅ PostgreSQL wznowiony"