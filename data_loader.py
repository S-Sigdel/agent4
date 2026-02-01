import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

DB_NAME = "employeeinfo"

def get_client():
    apikey = os.getenv("CLOUDANT_APIKEY")
    url = os.getenv("CLOUDANT_URL")
    auth_type = os.getenv("CLOUDANT_AUTH_TYPE", "iam")

    if not apikey or not url:
        raise ValueError("CLOUDANT_APIKEY and CLOUDANT_URL must be set in environment")

    if auth_type.lower() != "iam":
        raise NotImplementedError("Only IAM auth is implemented in this example.")

    authenticator = IAMAuthenticator(apikey)
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(url)
    return service

def load_employees():
    client = get_client()
    resp = client.post_all_docs(db=DB_NAME, include_docs=True).get_result()
    employees = []
    for row in resp["rows"]:
        doc = row.get("doc")
        if not doc:
            continue
        emp_rec = doc.get("employee_record")
        if not emp_rec:
            continue
        summary = ""
        skills = []

        # optional: build summary string
        jira = emp_rec.get("contributions", {}).get("jira", {})
        summary += jira.get("summary_jira", "")
        gitlab = emp_rec.get("contributions", {}).get("gitlab", {})
        summary += " " + gitlab.get("summary_gitlab", "")

        # example: collect skills from components
        skills = jira.get("components", [])

        employees.append({
            "employee_id": emp_rec.get("employee_id"),
            "summary": summary.strip(),
            "skills": skills,
            "raw_doc": doc
        })
    return employees
