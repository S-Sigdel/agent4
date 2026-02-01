#!/usr/bin/env python3
"""Test script to verify all components work"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("TESTING AGENT 4 - EMPLOYEE SEARCH MICROSERVICE")
print("=" * 60)

# Test 1: Check environment variables
print("\n1. Checking environment variables...")
required_vars = ["CLOUDANT_APIKEY", "CLOUDANT_URL", "OPENAI_API_KEY"]
missing_vars = []

for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✅ {var}: {'*' * 10} (set)")
    else:
        print(f"❌ {var}: NOT SET")
        missing_vars.append(var)

if missing_vars:
    print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
    print("Please set them in .env file")
    exit(1)

# Test 2: Test Cloudant connection
print("\n2. Testing Cloudant connection...")
try:
    from ibmcloudant.cloudant_v1 import CloudantV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    
    authenticator = IAMAuthenticator(os.getenv("CLOUDANT_APIKEY"))
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(os.getenv("CLOUDANT_URL"))
    
    dbs = service.get_all_dbs().get_result()
    print(f"✅ Connected to Cloudant!")
    print(f"   Available databases: {dbs}")
    
    if "employeeinfo" in dbs:
        print(f"✅ Database 'employeeinfo' found")
        docs = service.post_all_docs(db="employeeinfo", include_docs=True, limit=1).get_result()
        if docs.get("rows"):
            print(f"✅ Successfully fetched sample document")
        else:
            print(f"⚠️  Database is empty")
    else:
        print(f"❌ Database 'employeeinfo' not found")
        
except Exception as e:
    print(f"❌ Cloudant test failed: {e}")
    exit(1)

# Test 3: Test data loader
print("\n3. Testing data loader...")
try:
    from data_loader import load_employees
    employees = load_employees()
    print(f"✅ Loaded {len(employees)} employees")
    if employees:
        emp = employees[0]
        print(f"   Sample employee: {emp['employee_id']}")
        print(f"   Skills: {emp['skills']}")
except Exception as e:
    print(f"❌ Data loader test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Test embedder
print("\n4. Testing OpenAI embeddings...")
try:
    from embedder import embed
    test_text = "Python developer with FastAPI experience"
    embedding = embed(test_text)
    print(f"✅ Generated embedding")
    print(f"   Dimension: {len(embedding)}")
    print(f"   First 5 values: {embedding[:5]}")
except Exception as e:
    print(f"❌ Embedder test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Test vector store
print("\n5. Testing vector store...")
try:
    from vector_store import create_index, upsert_employee, search
    
    dim = len(embedding)
    index = create_index(dim)
    
    # Add sample employee
    upsert_employee(index, embedding, {
        "employee_id": "test_emp",
        "skills": ["Python", "FastAPI"]
    })
    
    # Search
    results = search(index, embedding, top_k=1)
    print(f"✅ Vector store working")
    print(f"   Search results: {results}")
except Exception as e:
    print(f"❌ Vector store test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\nYou can now start the server with:")
print("  uvicorn main:app --reload")
print("\nOr test with:")
print('  curl -X POST http://localhost:8000/search \\')
print('    -H "Content-Type: application/json" \\')
print('    -d \'{"role_description": "Python backend developer", "top_k": 5}\'')
