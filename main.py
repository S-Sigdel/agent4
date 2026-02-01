from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from data_loader import load_employees
from embedder import embed
from vector_store import create_index, upsert_employee, search

app = FastAPI(
    title="Agent 4 - Semantic Employee Search",
    description="Vector search microservice for employee intelligence. Designed for Watsonx Orchestrate.",
    version="1.0.0",
    servers=[
        {"url": "http://localhost:8000", "description": "Local Development Server"},
        {"url": "https://agent4.25rzrg3n3gow.us-south.codeengine.appdomain.cloud", "description": "Production Server"}
    ]
)

# Initialize index (dimension of embedding)
DIM = 3072  # text-embedding-3-large vector size
INDEX = create_index(DIM)
EMPLOYEES_DATA = {}  # Store full employee data for profile lookups

class SearchRequest(BaseModel):
    role_description: str = Field(..., description="Job description to search for matching employees")
    top_k: int = Field(5, ge=1, le=50, description="Number of top matches to return")

class SearchResponse(BaseModel):
    matches: List[Dict[str, Any]]

class ProfileResponse(BaseModel):
    employee_id: str
    summary: str
    skills: List[str]
    raw_doc: Optional[Dict[str, Any]] = None

@app.on_event("startup")
def startup_event():
    """On startup, fetch employees and index embeddings"""
    global EMPLOYEES_DATA
    
    try:
        employees = load_employees()
        for emp in employees:
            # Store full employee data for profile lookups
            EMPLOYEES_DATA[emp["employee_id"]] = emp
            
            # Create searchable text
            text = emp["summary"] + " Skills: " + ", ".join(emp["skills"])
            emb = embed(text)
            upsert_employee(INDEX, emb, emp)
        
        print(f"✅ Indexed {len(employees)} employees")
    except Exception as e:
        print(f"❌ Error during startup indexing: {e}")
        raise

@app.get("/", operation_id="health_check", summary="Health Check")
def root():
    """Health check endpoint to verify service status."""
    return {
        "service": "Agent 4 - Semantic Employee Search",
        "status": "running",
        "indexed_employees": len(EMPLOYEES_DATA)
    }

@app.post("/search", response_model=SearchResponse, operation_id="search_employees", summary="Search for Employees")
def search_employees(request: SearchRequest):
    """
    Search for employees matching a natural language job description or query.
    Returns a list of top matching candidates with relevance scores.
    """
    try:
        if not request.role_description.strip():
            raise HTTPException(status_code=400, detail="role_description cannot be empty")
        
        query_emb = embed(request.role_description)
        results = search(INDEX, query_emb, request.top_k)
        return {"matches": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/profile/{employee_id}", response_model=ProfileResponse, operation_id="get_employee_profile", summary="Get Employee Profile")
def get_employee_profile(employee_id: str):
    """
    Fetch detailed profile information for a specific employee by their ID.
    Includes skills, contribution summary, and raw record data.
    """
    if employee_id not in EMPLOYEES_DATA:
        raise HTTPException(status_code=404, detail=f"Employee '{employee_id}' not found")
    
    emp = EMPLOYEES_DATA[employee_id]
    return {
        "employee_id": emp["employee_id"],
        "summary": emp["summary"],
        "skills": emp["skills"],
        "raw_doc": emp.get("raw_doc")
    }
