"""
Simple test to call a Dynatrace MCP tool directly
This uses subprocess to avoid async complexity issues
"""

import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_mcp_tool():
    """Test calling an MCP tool using direct subprocess communication"""
    
    dt_environment = os.getenv("DT_ENVIRONMENT")
    dt_token = os.getenv("DT_PLATFORM_TOKEN")
    
    if not dt_environment or not dt_token:
        print("❌ Error: DT_ENVIRONMENT and DT_PLATFORM_TOKEN must be set")
        return
    
    print("=" * 80)
    print("Testing Dynatrace MCP Server Tool")
    print("=" * 80)
    print(f"\nEnvironment: {dt_environment}\n")
    
    # Prepare MCP request to list tools
    mcp_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    print("Sending request to MCP server...")
    print(f"Request: {json.dumps(mcp_request, indent=2)}\n")
    
    try:
        # Start the MCP server process
        env = os.environ.copy()
        env["DT_ENVIRONMENT"] = dt_environment
        env["DT_PLATFORM_TOKEN"] = dt_token
        
        process = subprocess.Popen(
            ["npx", "-y", "@dynatrace-oss/dynatrace-mcp-server@latest"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True
        )
        
        # Send the request
        request_str = json.dumps(mcp_request) + "\n"
        stdout, stderr = process.communicate(input=request_str, timeout=30)
        
        print("Response received!")
        print("-" * 80)
        
        # Parse response
        if stdout:
            try:
                # MCP responses might have multiple lines, get the last JSON
                lines = [line.strip() for line in stdout.split('\n') if line.strip()]
                for line in lines:
                    if line.startswith('{'):
                        response = json.loads(line)
                        if 'result' in response and 'tools' in response['result']:
                            tools = response['result']['tools']
                            print(f"\n✅ Found {len(tools)} tools:\n")
                            for idx, tool in enumerate(tools, 1):
                                print(f"{idx}. {tool['name']}")
                                print(f"   {tool.get('description', 'No description')}\n")
                            return
                        else:
                            print(f"Response: {json.dumps(response, indent=2)}")
            except json.JSONDecodeError as e:
                print(f"Could not parse JSON response: {e}")
                print(f"Raw output: {stdout[:500]}")
        
        if stderr:
            print(f"\nServer output:\n{stderr[:500]}")
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: MCP server did not respond in time")
        process.kill()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_mcp_tool()
