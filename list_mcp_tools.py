"""
List all available tools from the Dynatrace MCP Server running in VS Code
This script connects to the MCP server via stdio and retrieves all available tools
"""

import asyncio
import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("❌ Error: MCP library not installed.")
    print("Install it with: pip install mcp")
    exit(1)

# Fix for Windows event loop policy
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


async def list_mcp_tools():
    """Connect to Dynatrace MCP Server and list all available tools"""
    
    # Get environment variables
    dt_environment = os.getenv("DT_ENVIRONMENT")
    dt_token = os.getenv("DT_PLATFORM_TOKEN")
    
    if not dt_environment or not dt_token:
        print("❌ Error: DT_ENVIRONMENT and DT_PLATFORM_TOKEN must be set in .env file")
        return
    
    print("=" * 80)
    print("Dynatrace MCP Server - Available Tools")
    print("=" * 80)
    print(f"\nEnvironment: {dt_environment}")
    print("Starting MCP server connection...\n")
    
    # Configure MCP server parameters
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@dynatrace-oss/dynatrace-mcp-server@latest"],
        env={
            "DT_ENVIRONMENT": dt_environment,
            "DT_PLATFORM_TOKEN": dt_token,
        }
    )
    
    try:
        # Connect to MCP server
        print("Connecting to MCP server via stdio...")
        async with stdio_client(server_params) as (read, write):
            print("Creating client session...")
            async with ClientSession(read, write) as session:
                # Initialize session
                print("Initializing MCP session...")
                try:
                    init_result = await asyncio.wait_for(session.initialize(), timeout=30.0)
                    print(f"✅ Session initialized: {init_result}\n")
                except asyncio.TimeoutError:
                    print("❌ Timeout during initialization")
                    return
                
                # List all available tools
                print("Fetching available tools...")
                try:
                    tools_response = await asyncio.wait_for(session.list_tools(), timeout=15.0)
                except asyncio.TimeoutError:
                    print("❌ Timeout while fetching tools")
                    return
                
                tools = tools_response.tools
                print(f"✅ Found {len(tools)} available tools\n")
                print("=" * 80)
                
                # Display each tool with details
                for idx, tool in enumerate(tools, 1):
                    print(f"\n{idx}. {tool.name}")
                    print(f"   Description: {tool.description}")
                    
                    # Display parameters if available
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        schema = tool.inputSchema
                        if isinstance(schema, dict):
                            properties = schema.get('properties', {})
                            required = schema.get('required', [])
                            
                            if properties:
                                print(f"   Parameters:")
                                for param_name, param_info in properties.items():
                                    param_type = param_info.get('type', 'unknown')
                                    param_desc = param_info.get('description', 'No description')
                                    is_required = " (required)" if param_name in required else " (optional)"
                                    print(f"      • {param_name} ({param_type}){is_required}")
                                    if param_desc != 'No description':
                                        print(f"        {param_desc}")
                    
                    print("-" * 80)
                
                # Save to JSON file
                tools_data = []
                for tool in tools:
                    tool_dict = {
                        "name": tool.name,
                        "description": tool.description,
                    }
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        tool_dict["inputSchema"] = tool.inputSchema
                    tools_data.append(tool_dict)
                
                output_file = "mcp_tools.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(tools_data, f, indent=2)
                
                # Summary
                print(f"\n📊 Summary:")
                print(f"   Total tools: {len(tools)}")
                print(f"   Environment: {dt_environment}")
                print(f"   Output saved to: {output_file}")
                
                # Categorize tools for the assignment
                print(f"\n🎯 Key Tools for Your Assignment:")
                print(f"   (Finding problems, vulnerabilities, and logs)")
                
                key_tools = {
                    "list_problems": "Find all open problems",
                    "list_vulnerabilities": "Find security vulnerabilities",
                    "execute_dql": "Query logs and events",
                    "find_entity_by_name": "Discover entity IDs",
                    "get_environment_info": "Verify connection"
                }
                
                for tool in tools:
                    if tool.name in key_tools:
                        print(f"   ✓ {tool.name} - {key_tools[tool.name]}")
                
                print("\n" + "=" * 80)
                print("✅ Tool listing complete!")
                print("=" * 80)
                
                # Test calling a tool
                print("\n🧪 Testing a tool: get_environment_info")
                print("-" * 80)
                try:
                    result = await asyncio.wait_for(
                        session.call_tool("get_environment_info", {}),
                        timeout=10.0
                    )
                    print("✅ Tool call successful!")
                    print(f"Result: {result}")
                except asyncio.TimeoutError:
                    print("❌ Timeout while calling tool")
                except Exception as e:
                    print(f"❌ Error calling tool: {str(e)}")
                
                print("=" * 80)
                
    except asyncio.TimeoutError:
        print("\n❌ Timeout: MCP server took too long to respond")
        print("   The server may be running but not responding to requests")
        print("   Check your Dynatrace credentials and network connection")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(f"   Type: {type(e).__name__}")
        print("\nTroubleshooting:")
        print("   1. Ensure Node.js and npm are installed")
        print("   2. Verify DT_ENVIRONMENT and DT_PLATFORM_TOKEN in .env")
        print("   3. Check network connectivity to Dynatrace")


def main():
    """Main entry point"""
    try:
        # Create new event loop to avoid issues
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(list_mcp_tools())
        finally:
            loop.close()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
    except ExceptionGroup as eg:
        print(f"\n❌ Multiple errors occurred:")
        for i, exc in enumerate(eg.exceptions, 1):
            print(f"   {i}. {type(exc).__name__}: {str(exc)}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print(f"   Type: {type(e).__name__}")


if __name__ == "__main__":
    main()
