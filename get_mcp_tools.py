"""
Get all available tools from Dynatrace MCP Server
This version uses a more robust approach to handle MCP protocol
"""

import asyncio
import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()

# Check if MCP is installed
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️  MCP library not available. Install with: pip install mcp")

# Windows event loop fix
if sys.platform == 'win32' and MCP_AVAILABLE:
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except:
        pass


async def get_tools_from_mcp():
    """Get tools from MCP server"""
    dt_environment = os.getenv("DT_ENVIRONMENT")
    dt_token = os.getenv("DT_PLATFORM_TOKEN")
    
    if not dt_environment or not dt_token:
        print("❌ Missing DT_ENVIRONMENT or DT_PLATFORM_TOKEN")
        return None
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@dynatrace-oss/dynatrace-mcp-server@latest"],
        env={
            "DT_ENVIRONMENT": dt_environment,
            "DT_PLATFORM_TOKEN": dt_token,
            "DT_MCP_DISABLE_TELEMETRY": "true"  # Disable telemetry to reduce noise
        }
    )
    
    tools_list = []
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                
                # Get tools
                response = await session.list_tools()
                tools_list = response.tools
                
                return tools_list
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)}")
        return None


def display_tools(tools):
    """Display tools in a formatted way"""
    if not tools:
        print("No tools found")
        return
    
    print(f"\n{'='*80}")
    print(f"Found {len(tools)} Dynatrace MCP Tools")
    print(f"{'='*80}\n")
    
    for idx, tool in enumerate(tools, 1):
        print(f"{idx}. {tool.name}")
        print(f"   Description: {tool.description}")
        
        if hasattr(tool, 'inputSchema') and tool.inputSchema:
            schema = tool.inputSchema
            if isinstance(schema, dict) and 'properties' in schema:
                props = schema['properties']
                required = schema.get('required', [])
                print(f"   Parameters:")
                for param, info in props.items():
                    req = "(required)" if param in required else "(optional)"
                    ptype = info.get('type', 'unknown')
                    print(f"      • {param} {req} - {ptype}")
        print()
    
    # Save to file
    tools_data = []
    for tool in tools:
        tool_dict = {
            "name": tool.name,
            "description": tool.description
        }
        if hasattr(tool, 'inputSchema'):
            tool_dict["inputSchema"] = tool.inputSchema
        tools_data.append(tool_dict)
    
    with open("mcp_tools.json", "w") as f:
        json.dump(tools_data, f, indent=2)
    
    print(f"{'='*80}")
    print("✅ Tools saved to mcp_tools.json")
    print(f"{'='*80}\n")
    
    # Show key tools for assignment
    print("🎯 Key tools for your assignment:")
    key_tools = ["list_problems", "list_vulnerabilities", "execute_dql", 
                 "find_entity_by_name", "get_environment_info"]
    for tool in tools:
        if tool.name in key_tools:
            print(f"   ✓ {tool.name}")


def main():
    if not MCP_AVAILABLE:
        print("\n❌ Cannot proceed without MCP library")
        print("Install it with: pip install mcp")
        return
    
    print("Connecting to Dynatrace MCP Server...")
    print("(This may take a moment...)\n")
    
    try:
        # Run with proper event loop handling
        if sys.platform == 'win32':
            # Windows-specific handling
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                tools = loop.run_until_complete(get_tools_from_mcp())
            finally:
                loop.close()
        else:
            # Unix/Linux
            tools = asyncio.run(get_tools_from_mcp())
        
        if tools:
            display_tools(tools)
        else:
            print("❌ Failed to retrieve tools")
            
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
