#!/bin/bash

echo "🧪 Testing Agent 4 API..."
echo ""

# Test 1: Health check
echo "1️⃣  Testing health check (GET /)..."
curl -s http://localhost:8000/ | jq '.'
echo ""
echo ""

# Test 2: Search for employees
echo "2️⃣  Testing employee search (POST /search)..."
curl -s -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "role_description": "Python backend developer with microservices experience",
    "top_k": 3
  }' | jq '.'
echo ""
echo ""

# Test 3: Another search
echo "3️⃣  Testing another search - Frontend developer..."
curl -s -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "role_description": "Frontend developer with React and JavaScript",
    "top_k": 3
  }' | jq '.'
echo ""
echo ""

# Test 4: Get employee profile (you'll need to use an actual employee_id from search results)
echo "4️⃣  To test profile endpoint, use an employee_id from the search results:"
echo "   curl http://localhost:8000/profile/employee177 | jq '.'"
echo ""

echo "✅ API tests complete!"
