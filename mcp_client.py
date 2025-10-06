import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Load environment variables from a local .env file (if present) and the system env
load_dotenv()

async def list_mcp_tools():
    """Connect to Dynatrace MCP server and list all available tools."""
    
    # Configure server parameters matching your VS Code config
    # Read sensitive values from environment (prefers .env if present)
    dt_token = os.getenv("DT_PLATFORM_TOKEN")
    dt_env = os.getenv("DT_ENVIRONMENT")

    env_vars = {}
    if dt_token:
        env_vars["DT_PLATFORM_TOKEN"] = dt_token
    if dt_env:
        env_vars["DT_ENVIRONMENT"] = dt_env

    if not env_vars:
        # If neither value is provided, warn the user but continue; the server
        # may still read values from other places depending on config.
        print("Warning: DT_PLATFORM_TOKEN and DT_ENVIRONMENT are not set in environment or .env file.")

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@dynatrace-oss/dynatrace-mcp-server@latest"],
        env=env_vars
    )
    
    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List all available tools
            tools = await session.list_tools()
            
            print("Available MCP Tools:\n")
            print("=" * 80)
            
            for tool in tools.tools:
                print(f"\nTool: {tool.name}")
                print(f"Description: {tool.description}")
                
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print("\nInput Schema:")
                    if 'properties' in tool.inputSchema:
                        for param_name, param_info in tool.inputSchema['properties'].items():
                            required = param_name in tool.inputSchema.get('required', [])
                            req_str = " (required)" if required else " (optional)"
                            param_type = param_info.get('type', 'any')
                            param_desc = param_info.get('description', 'No description')
                            print(f"  - {param_name}{req_str}: {param_type}")
                            print(f"    {param_desc}")
                
                print("-" * 80)
            
            print(f"\nTotal tools available: {len(tools.tools)}")
            
            return tools.tools

if __name__ == "__main__":
    # Run the async function
    asyncio.run(list_mcp_tools())