import json
import os
from main import app

def generate_openapi():
    print("Generating OpenAPI schema...")
    
    # Get the schema from FastAPI
    openapi_schema = app.openapi()
    
    # Ensure correct OpenApi version for compatibility (3.0.x is widely supported)
    openapi_schema["openapi"] = "3.0.3"
    
    # Write to file
    output_file = "openapi.json"
    with open(output_file, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"✅ Schema saved to: {os.path.abspath(output_file)}")
    print("\nNext steps:")
    print("1. If deploying to cloud, update the 'servers' url in openapi.json to your public HTTPS URL.")
    print("2. Import this file into IBM Watsonx Orchestrate as a custom API skill.")

if __name__ == "__main__":
    generate_openapi()