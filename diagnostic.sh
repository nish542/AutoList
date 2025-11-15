#!/bin/bash

echo "=========================================="
echo "API Connection Diagnostic Tool"
echo "=========================================="
echo ""

# Test if backend is running
echo "1. Testing backend server on localhost:8000..."
if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "   ✅ Backend is running"
else
    echo "   ❌ Backend is NOT running"
    echo "   Start it with: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
fi

echo ""

# Test GET /categories endpoint
echo "2. Testing GET /categories endpoint..."
CATEGORIES_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/categories)
if [ "$CATEGORIES_RESPONSE" = "200" ]; then
    echo "   ✅ GET /categories is working (HTTP $CATEGORIES_RESPONSE)"
    curl -s http://localhost:8000/categories | head -c 200
    echo "   ..."
else
    echo "   ❌ GET /categories returned HTTP $CATEGORIES_RESPONSE"
fi

echo ""
echo ""

# Test POST /generate endpoint (minimal test)
echo "3. Testing POST /generate endpoint..."
GENERATE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -F "text_content=Test product" \
  http://localhost:8000/generate)

if [ "$GENERATE_RESPONSE" = "200" ] || [ "$GENERATE_RESPONSE" = "500" ]; then
    echo "   ✅ POST /generate endpoint exists (HTTP $GENERATE_RESPONSE)"
    echo "   Note: 500 error is expected if dependencies aren't fully loaded"
else
    echo "   ❌ POST /generate returned HTTP $GENERATE_RESPONSE"
fi

echo ""
echo "=========================================="
echo "Frontend Configuration:"
echo "=========================================="
echo "Check if these ports are in use:"
echo ""

# Check port 5173 (frontend)
if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "   ✅ Port 5173 (Frontend) is in use"
else
    echo "   ❌ Port 5173 (Frontend) is NOT in use"
    echo "   Start it with: cd frontend && npm run dev"
fi

echo ""

# Check port 8000 (backend)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "   ✅ Port 8000 (Backend) is in use"
else
    echo "   ❌ Port 8000 (Backend) is NOT in use"
    echo "   Start it with: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
fi

echo ""
echo "=========================================="
