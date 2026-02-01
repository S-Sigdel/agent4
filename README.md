# Agent 4 - Semantic Employee Search Microservice

A FastAPI-based vector search microservice for intelligent employee matching using OpenAI embeddings and FAISS.

## Overview

This service connects to IBM Cloudant to fetch employee records, generates semantic embeddings using OpenAI, and provides fast similarity search to match job descriptions with qualified candidates.

## Features

- ✅ **Cloudant Integration** - Automatically fetches employee data from IBM Cloudant
- ✅ **OpenAI Embeddings** - Uses `text-embedding-3-large` for semantic understanding
- ✅ **FAISS Vector Search** - Lightning-fast similarity search
- ✅ **FastAPI** - Modern async API with automatic documentation
- ✅ **Dynamic Indexing** - Indexes all employees on startup
- ✅ **Profile Lookup** - Fetch detailed employee information by ID

## Prerequisites

- Python 3.12+
- IBM Cloudant account with `employeeinfo` database
- OpenAI API key

## Installation

1. **Clone/navigate to the project:**
```bash
cd /home/thinking/agent4
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Create or edit `.env` file:
```env
CLOUDANT_APIKEY=your_cloudant_api_key
CLOUDANT_URL=your_cloudant_url
CLOUDANT_AUTH_TYPE=iam
OPENAI_API_KEY=your_openai_api_key
```

## Testing

**Test all components:**
```bash
python test_setup.py
```

**Test Cloudant connection only:**
```bash
python test_conn.py
```

## Running the Service

**Start the server:**
```bash
uvicorn main:app --reload
```

The service will:
1. Load environment variables
2. Connect to Cloudant
3. Fetch all employee records
4. Generate embeddings for each employee
5. Index them in FAISS
6. Start the API server on http://localhost:8000

## API Endpoints

### 1. Health Check
```bash
GET /
```

**Response:**
```json
{
  "service": "Agent 4 - Semantic Employee Search",
  "status": "running",
  "indexed_employees": 150
}
```

### 2. Search Employees
```bash
POST /search
```

**Request:**
```json
{
  "role_description": "Senior backend engineer with Kafka and microservices experience",
  "top_k": 5
}
```

**Response:**
```json
{
  "matches": [
    {
      "employee_id": "employee177",
      "score": 0.1234,
      "skills": ["Kafka", "Microservices", "Python"]
    }
  ]
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "role_description": "Python developer with FastAPI experience",
    "top_k": 5
  }'
```

### 3. Get Employee Profile
```bash
GET /profile/{employee_id}
```

**Response:**
```json
{
  "employee_id": "employee177",
  "summary": "Worked on 7 Jira issues including 1 bug...",
  "skills": ["payments-service", "android-app"],
  "raw_doc": { ... }
}
```

**cURL Example:**
```bash
curl http://localhost:8000/profile/employee177
```

### 4. Interactive API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Architecture

```
┌─────────────────┐
│   Watsonx       │
│   Orchestrate   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   FastAPI       │─────▶│   OpenAI     │
│   Endpoints     │      │   Embeddings │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   FAISS Vector  │      │   Cloudant   │
│   Store         │◀─────│   Database   │
└─────────────────┘      └──────────────┘
```

## Files

- **main.py** - FastAPI application with endpoints
- **cloudant_client.py** - Cloudant connection utilities
- **data_loader.py** - Fetches and processes employee data
- **embedder.py** - OpenAI embedding generation
- **vector_store.py** - FAISS index management
- **test_conn.py** - Tests Cloudant connection
- **test_setup.py** - Comprehensive test suite
- **requirements.txt** - Python dependencies
- **.env** - Environment variables (do not commit!)

## Potential Pitfalls Fixed

✅ **Environment Variable Naming** - Fixed inconsistent naming (OPENAI_API_KEY vs OPENAI_APIKEY)  
✅ **OpenAI API Version** - Updated from deprecated `openai.Embedding.create()` to new client pattern  
✅ **Import Errors** - Fixed wrong function imports in main.py  
✅ **Missing Dependencies** - Added faiss-cpu to requirements.txt  
✅ **Case Sensitivity** - Fixed lowercase vs uppercase env vars in data_loader.py  
✅ **Error Handling** - Added validation for missing environment variables  
✅ **Type Safety** - Added Pydantic models for request/response validation  

## Development

**Enable auto-reload during development:**
```bash
uvicorn main:app --reload --log-level debug
```

## Production Considerations

For production deployment:
1. Use environment variables from a secrets manager
2. Enable CORS if called from web frontends
3. Add authentication/authorization
4. Implement rate limiting
5. Add monitoring and logging
6. Consider persistent FAISS index storage
7. Implement incremental index updates for new employees
8. Add health check endpoints for orchestration platform

## Troubleshooting

**Issue: "CLOUDANT_APIKEY not set"**
- Ensure `.env` file exists and variables are set
- Source the file or use `python-dotenv`

**Issue: "Module not found"**
- Run `pip install -r requirements.txt`

**Issue: "OpenAI API error"**
- Verify your OPENAI_API_KEY is valid
- Check API usage limits

**Issue: "Database 'employeeinfo' not found"**
- Verify Cloudant credentials
- Ensure database exists and is accessible

## License

MIT
