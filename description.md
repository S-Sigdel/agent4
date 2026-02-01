

# Agent 4 — Semantic Employee Search Microservice

## Purpose

Agent 4 is a **vector search microservice** for employee intelligence.
It **connects to a Cloudant database**, generates **semantic embeddings** using **OpenAI**, and supports **searching employees** by a job description.

It is **designed to be called from Watsonx Orchestrate**, not directly by a frontend.

---

## Data Source

* Database: `employeeinfo` on IBM Cloudant
* Each document is **normalized** like:

```json
{
  "_id": "27401351bcd0c923ad08746c993296e6",
  "employee_record": {
    "employee_id": "employee177",
    "contributions": {
      "jira": {
        "summary_jira": "Worked on 7 Jira issues including 1 bug, 4 tasks, and 2 stories...",
        "components": ["payments-service", "android-app"],
        "projects": ["Analytics", "Customer Experience"]
      },
      "gitlab": {
        "summary_gitlab": "No GitLab contribution activity found for this employee."
      }
    }
  }
}
```

* The microservice dynamically fetches all documents from Cloudant (using `CLOUDANT_APIKEY`, `CLOUDANT_URL`) and converts them into **searchable vectors**.
* No hardcoding of employee data.

---

## Core Features

1. **Cloudant Integration**

   * Pulls all employee records automatically.
   * Supports IAM authentication using environment variables:

     * `CLOUDANT_APIKEY`
     * `CLOUDANT_URL`
     * `CLOUDANT_AUTH_TYPE` (default: IAM)

2. **Embeddings**

   * Uses OpenAI `text-embedding-3-large`.
   * Environment variable for API key: `OPENAI_APIKEY`.

3. **Vector Store**

   * FAISS used as a lightweight in-memory vector index.
   * Stores employee embeddings with metadata for fast similarity search.

4. **Endpoints (FastAPI)**

   * `/search` → input a job description, returns top N candidates.
   * Optional: `/profile` → fetch employee metadata.

5. **Dynamic Updates**

   * On startup, pulls all documents and indexes them.
   * Ready to be extended for auto-indexing new documents from Cloudant.

---

## Usage

```bash
export CLOUDANT_APIKEY="..."
export CLOUDANT_URL="..."
export OPENAI_APIKEY="..."
uvicorn main:app --reload
```

**Search Example:**

```json
POST /search
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
      "skills": ["Kafka", "Microservices"]
    },
    ...
  ]
}
```

---

## Tech Stack

* Python 3.12+
* FastAPI
* IBM Cloudant SDK (`ibmcloudant`)
* OpenAI embeddings
* FAISS vector store

---

## Goal for Copilot

* Build endpoints for `/search`, `/profile`
* Automatically index Cloudant documents into FAISS
* Generate embeddings using OpenAI
* Support **dynamic updates** whenever new employees are added
* Keep code **hackathon-friendly**, readable, and production-adjacent

---

The, if you source the .env you will get all the things put up. 