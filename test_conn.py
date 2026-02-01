import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

DB_NAME = "employeeinfo"

def test_connection():
    try:
        # Load credentials from environment
        apikey = os.getenv("CLOUDANT_APIKEY")
        url = os.getenv("CLOUDANT_URL")
        auth_type = os.getenv("CLOUDANT_AUTH_TYPE", "iam")

        if not apikey or not url:
            raise ValueError("CLOUDANT_APIKEY or CLOUDANT_URL not set in environment")

        if auth_type.lower() != "iam":
            raise NotImplementedError("Only IAM auth is implemented in this test")

        # Create client
        authenticator = IAMAuthenticator(apikey)
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(url)

        # Try to get database info
        resp = service.get_all_dbs().get_result()
        print("✅ Successfully connected to Cloudant!")
        print(f"Available databases: {resp}")

        # Optionally, check your target database
        if DB_NAME in resp:
            print(f"✅ Database '{DB_NAME}' exists and is accessible.")
            # Fetch a single doc to verify read
            docs = service.post_all_docs(db=DB_NAME, include_docs=True, limit=1).get_result()
            print("Sample document fetched:")
            print(docs["rows"][0].get("doc"))
        else:
            print(f"❌ Database '{DB_NAME}' not found.")
    except Exception as e:
        print(f"❌ Cloudant connection test failed: {e}")

if __name__ == "__main__":
    test_connection()
