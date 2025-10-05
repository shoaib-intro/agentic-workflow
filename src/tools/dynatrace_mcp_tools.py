"""
Dynatrace MCP Tools - CrewAI-compatible tools that use the Dynatrace MCP Server
These tools wrap MCP server calls to be used by CrewAI agents
"""

import os
import asyncio
import sys
from typing import Dict, Any, Optional
from crewai_tools import BaseTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import MCP client
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP library not installed. Install with: pip install mcp")

# Windows event loop fix
if sys.platform == 'win32' and MCP_AVAILABLE:
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except:
        pass


class MCPClient:
    """Singleton MCP client for reusing connections"""
    _instance = None
    _session = None
    _read = None
    _write = None
    _client_context = None
    
    @classmethod
    async def get_session(cls):
        """Get or create MCP session"""
        if cls._session is None:
            dt_environment = os.getenv("DT_ENVIRONMENT")
            dt_token = os.getenv("DT_PLATFORM_TOKEN")
            
            if not dt_environment or not dt_token:
                raise ValueError("DT_ENVIRONMENT and DT_PLATFORM_TOKEN must be set")
            
            server_params = StdioServerParameters(
                command="npx",
                args=["-y", "@dynatrace-oss/dynatrace-mcp-server@latest"],
                env={
                    "DT_ENVIRONMENT": dt_environment,
                    "DT_PLATFORM_TOKEN": dt_token,
                    "DT_MCP_DISABLE_TELEMETRY": "true"
                }
            )
            
            cls._client_context = stdio_client(server_params)
            cls._read, cls._write = await cls._client_context.__aenter__()
            
            session_context = ClientSession(cls._read, cls._write)
            cls._session = await session_context.__aenter__()
            await cls._session.initialize()
        
        return cls._session
    
    @classmethod
    async def close(cls):
        """Close MCP session"""
        if cls._session:
            try:
                await cls._session.__aexit__(None, None, None)
            except:
                pass
            cls._session = None
        
        if cls._client_context:
            try:
                await cls._client_context.__aexit__(None, None, None)
            except:
                pass
            cls._client_context = None


def run_async(coro):
    """Helper to run async code in sync context"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Create new loop in thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # No event loop, create new one
        return asyncio.run(coro)


class ListProblemsTool(BaseTool):
    name: str = "List Dynatrace Problems"
    description: str = (
        "List all open problems from Dynatrace for the last 12 hours. "
        "Use this to identify active issues affecting services and infrastructure. "
        "Returns problems with severity, status, and affected entities."
    )
    
    def _run(self, additional_filter: str = "", max_problems: int = 25) -> str:
        """List problems using MCP server"""
        async def list_problems():
            session = await MCPClient.get_session()
            result = await session.call_tool(
                "list_problems",
                {
                    "additionalFilter": additional_filter,
                    "maxProblemsToDisplay": max_problems
                }
            )
            return result
        
        try:
            result = run_async(list_problems())
            
            # Format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
                return str(content)
            return str(result)
            
        except Exception as e:
            return f"Error listing problems: {str(e)}\nMake sure the MCP server is accessible and credentials are correct."


class ListVulnerabilitiesTool(BaseTool):
    name: str = "List Dynatrace Vulnerabilities"
    description: str = (
        "List all active vulnerabilities from Dynatrace for the last 30 days. "
        "Use this to identify security risks, CVEs, and vulnerable components. "
        "Returns vulnerabilities with risk scores, affected entities, and remediation info."
    )
    
    def _run(self, risk_score: float = 8.0, additional_filter: str = "", max_vulnerabilities: int = 25) -> str:
        """List vulnerabilities using MCP server"""
        async def list_vulnerabilities():
            session = await MCPClient.get_session()
            result = await session.call_tool(
                "list_vulnerabilities",
                {
                    "riskScore": risk_score,
                    "additionalFilter": additional_filter,
                    "maxVulnerabilitiesToDisplay": max_vulnerabilities
                }
            )
            return result
        
        try:
            result = run_async(list_vulnerabilities())
            
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
                return str(content)
            return str(result)
            
        except Exception as e:
            return f"Error listing vulnerabilities: {str(e)}\nMake sure the MCP server is accessible and credentials are correct."


class ExecuteDQLTool(BaseTool):
    name: str = "Execute DQL Query"
    description: str = (
        "Execute a Dynatrace Query Language (DQL) query to fetch logs, events, spans, or metrics. "
        "Use this for custom queries to analyze specific data. "
        "Input should be a valid DQL query string. "
        "Example: 'fetch logs | filter status == \"ERROR\" | limit 10'"
    )
    
    def _run(self, dql_statement: str) -> str:
        """Execute DQL query using MCP server"""
        async def execute_dql():
            session = await MCPClient.get_session()
            result = await session.call_tool(
                "execute_dql",
                {"dqlStatement": dql_statement}
            )
            return result
        
        try:
            result = run_async(execute_dql())
            
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
                return str(content)
            return str(result)
            
        except Exception as e:
            return f"Error executing DQL: {str(e)}\nCheck your DQL syntax and try again."


class FindEntityByNameTool(BaseTool):
    name: str = "Find Entity by Name"
    description: str = (
        "Find the entityId and type of a monitored entity (service, host, process-group, etc.) based on name. "
        "Use this before querying logs or metrics for specific entities. "
        "Input should be the entity name to search for."
    )
    
    def _run(self, entity_name: str) -> str:
        """Find entity by name using MCP server"""
        async def find_entity():
            session = await MCPClient.get_session()
            result = await session.call_tool(
                "find_entity_by_name",
                {"entityName": entity_name}
            )
            return result
        
        try:
            result = run_async(find_entity())
            
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
                return str(content)
            return str(result)
            
        except Exception as e:
            return f"Error finding entity: {str(e)}"


class GetEnvironmentInfoTool(BaseTool):
    name: str = "Get Dynatrace Environment Info"
    description: str = (
        "Get information about the connected Dynatrace environment and verify the connection. "
        "Use this to confirm connectivity and get tenant details."
    )
    
    def _run(self) -> str:
        """Get environment info using MCP server"""
        async def get_env_info():
            session = await MCPClient.get_session()
            result = await session.call_tool("get_environment_info", {})
            return result
        
        try:
            result = run_async(get_env_info())
            
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
                return str(content)
            return str(result)
            
        except Exception as e:
            return f"Error getting environment info: {str(e)}"


class GenerateDQLTool(BaseTool):
    name: str = "Generate DQL from Natural Language"
    description: str = (
        "Convert natural language queries to Dynatrace Query Language (DQL) using Davis CoPilot AI. "
        "Use this when you need to create a DQL query but don't know the exact syntax. "
        "Input should be your question in plain English."
    )
    
    def _run(self, natural_language_query: str, context: str = "") -> str:
        """Generate DQL from natural language using MCP server"""
        async def generate_dql():
            session = await MCPClient.get_session()
            result = await session.call_tool(
                "generate_dql_from_natural_language",
                {
                    "naturalLanguageQuery": natural_language_query,
                    "context": context
                }
            )
            return result
        
        try:
            result = run_async(generate_dql())
            
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
                return str(content)
            return str(result)
            
        except Exception as e:
            return f"Error generating DQL: {str(e)}"


# Export all tools
__all__ = [
    'ListProblemsTool',
    'ListVulnerabilitiesTool',
    'ExecuteDQLTool',
    'FindEntityByNameTool',
    'GetEnvironmentInfoTool',
    'GenerateDQLTool'
]
