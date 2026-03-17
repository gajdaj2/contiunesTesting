#!/bin/bash

set -e

API="http://localhost:3000"

echo "================================"
echo "🧪 Testowanie Aplikacji"
echo "================================"
echo ""

# Test 1: Health check
echo "1️⃣  Health Check:"
curl -s $API/health | jq '.'
echo ""

# Test 2: Dane z bazy
echo "2️⃣  Dane z Bazy Danych:"
curl -s $API/users/db | jq '.' || echo "❌ Baza niedostępna"
echo ""

# Test 3: Cache
echo "3️⃣  Dane z Cache'u:"
curl -s $API/users/cached | jq '.' || echo "❌ Cache niedostępny"
echo ""

# Test 4: Queue
echo "4️⃣  Wysłanie Jobu do Queue:"
curl -s -X POST $API/jobs | jq '.' || echo "❌ Queue niedostępna"
echo ""

echo "✅ Test zakończony"