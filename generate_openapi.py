import json
import os
from main import app

def generate_openapi():
    print("Generating OpenAPI schema...")
    
    # Get the schema from FastAPI
    openapi_schema = app.openapi()
    
    # --- POST-PROCESSING FOR WATSONX COMPATIBILITY ---
    
    # 1. Set Version
    openapi_schema["openapi"] = "3.0.1"
    
    # 2. Filter Servers - Keep only the production one (if available), or the last one
    # Watsonx generally expects one URL.
    if "servers" in openapi_schema and len(openapi_schema["servers"]) > 1:
        # Prefer HTTPS/Cloud Engine URL if found
        kube_servers = [s for s in openapi_schema["servers"] if "codeengine.appdomain.cloud" in s["url"]]
        if kube_servers:
            openapi_schema["servers"] = kube_servers
        else:
            # Fallback to just keeping the last one (usually production in our list)
            openapi_schema["servers"] = [openapi_schema["servers"][-1]]

    # 3. Simplify Schemas (Fix 'anyOf' and empty objects)
    def clean_schema(schema_node):
        if isinstance(schema_node, dict):
            # Fix Pydantic's 'anyOf' null handling -> switch to nullable: true
            if "anyOf" in schema_node:
                # specific clean up for optional dictionaries
                types = [x.get("type") for x in schema_node["anyOf"] if "type" in x]
                if "object" in types and "null" in types:
                    del schema_node["anyOf"]
                    schema_node["type"] = "object"
                    schema_node["nullable"] = True
                    schema_node["additionalProperties"] = True
                # Clean up specific Pydantic ValidationError 'loc' which mixes string/int
                elif "string" in types and "integer" in types:
                     del schema_node["anyOf"]
                     schema_node["type"] = "string" # Simplify to string for compatibility

            # Recursive traversal
            for key, value in schema_node.items():
                clean_schema(value)
        elif isinstance(schema_node, list):
            for item in schema_node:
                clean_schema(item)

    clean_schema(openapi_schema)
    
    # 4. Explicitly fix Health Check empty schema
    try:
        paths = openapi_schema.get("paths", {})
        if "/" in paths and "get" in paths["/"]:
            resp = paths["/"]["get"]["responses"].get("200", {})
            content = resp.get("content", {}).get("application/json", {})
            if content.get("schema") == {}:
                content["schema"] = {"type": "object", "title": "HealthCheckResponse"}
    except Exception:
        pass

    # --- END POST-PROCESSING ---

    # Write to JSON file
    output_file_json = "openapi.json"
    with open(output_file_json, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"✅ JSON Schema saved to: {os.path.abspath(output_file_json)}")

    # Write to YAML file
    try:
        import yaml
        # Custom representer to handle indentation/block style better if needed, 
        # but default safe_dump is usually sufficient for OpenAPI
        
        # Ensure that long strings (like descriptions) use block style for readability
        def str_presenter(dumper, data):
            if len(data.splitlines()) > 1:  # check for multiline string
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)

        yaml.add_representer(str, str_presenter)

        output_file_yaml = "openapi.yaml"
        with open(output_file_yaml, "w") as f:
            yaml.dump(openapi_schema, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"✅ YAML Schema saved to: {os.path.abspath(output_file_yaml)}")
    except ImportError:
        print("⚠️ PyYAML not installed. Skipping YAML generation. Run 'pip install pyyaml'")
    
    print("\nNext steps:")
    print("1. If deploying to cloud, update the 'servers' url in openapi.json to your public HTTPS URL.")
    print("2. Import this file into IBM Watsonx Orchestrate as a custom API skill.")

if __name__ == "__main__":
    generate_openapi()