"""
Debug script to check actual MCP tool parameters
"""

import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

async def check_tool_schema():
    """Get the actual schema from MCP server"""
    dt_environment = os.getenv("DT_ENVIRONMENT")
    dt_token = os.getenv("DT_PLATFORM_TOKEN")
    
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@dynatrace-oss/dynatrace-mcp-server@latest"],
        env={
            "DT_ENVIRONMENT": dt_environment,
            "DT_PLATFORM_TOKEN": dt_token,
            "DT_MCP_DISABLE_TELEMETRY": "true"
        }
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get tools
            tools = await session.list_tools()
            
            # Find the problematic tools
            problem_tools = [
                "generate_dql_from_natural_language",
                "find_entity_by_name",
                "chat_with_davis_copilot"
            ]
            
            for tool in tools.tools:
                if tool.name in problem_tools:
                    print(f"\n{'='*80}")
                    print(f"Tool: {tool.name}")
                    print(f"{'='*80}")
                    print(f"Description: {tool.description}")
                    
                    if hasattr(tool, 'inputSchema'):
                        schema = tool.inputSchema
                        print(f"\nInput Schema:")
                        print(f"  Type: {schema.get('type', 'N/A')}")
                        
                        if 'properties' in schema:
                            print(f"  Properties:")
                            for prop_name, prop_info in schema['properties'].items():
                                print(f"    - {prop_name}:")
                                print(f"        type: {prop_info.get('type', 'N/A')}")
                                print(f"        description: {prop_info.get('description', 'N/A')}")
                        
                        if 'required' in schema:
                            print(f"  Required: {schema['required']}")

if __name__ == "__main__":
    asyncio.run(check_tool_schema())
