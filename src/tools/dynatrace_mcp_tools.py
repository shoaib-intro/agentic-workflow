"""
Dynatrace MCP Tools - Custom tools for CrewAI agents using Dynatrace MCP Server
These tools connect to the MCP server and call the available tools
"""

import asyncio
import os
from typing import Optional, Dict, Any
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️  MCP library not installed. Install with: pip install mcp")


class MCPClient:
    """Singleton client for MCP server connection"""
    _instance = None
    _session = None
    
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
            
            # This is a simplified version - in production you'd manage the connection lifecycle better
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    cls._session = session
                    return session
        
        return cls._session
    
    @classmethod
    async def call_tool(cls, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call an MCP tool"""
        session = await cls.get_session()
        result = await session.call_tool(tool_name, arguments)
        return result


def run_async(coro):
    """Helper to run async code in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)


# ============================================================================
# PROBLEM MANAGEMENT TOOLS
# ============================================================================

class ListProblemsTool(BaseTool):
    name: str = "List Dynatrace Problems"
    description: str = (
        "List all problems from Dynatrace for the last 12 hours. "
        "Use this to identify active issues affecting services and infrastructure. "
        "You can optionally filter by entity or limit the number of results."
    )
    
    def _run(self, additional_filter: str = "", max_problems: int = 25) -> str:
        """List problems from Dynatrace"""
        try:
            arguments = {}
            if additional_filter:
                arguments["additionalFilter"] = additional_filter
            if max_problems != 25:
                arguments["maxProblemsToDisplay"] = max_problems
            
            result = run_async(MCPClient.call_tool("list_problems", arguments))
            
            # Parse and format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
            
            return str(result)
            
        except Exception as e:
            return f"Error listing problems: {str(e)}"


# ============================================================================
# SECURITY TOOLS
# ============================================================================

class ListVulnerabilitiesTool(BaseTool):
    name: str = "List Dynatrace Vulnerabilities"
    description: str = (
        "Retrieve all active vulnerabilities from Dynatrace for the last 30 days. "
        "Use this to identify security risks, CVEs, and vulnerable components. "
        "You can filter by risk score (default: 8.0) or add custom filters."
    )
    
    def _run(self, risk_score: float = 8.0, additional_filter: str = "", max_vulnerabilities: int = 25) -> str:
        """List vulnerabilities from Dynatrace"""
        try:
            arguments = {}
            if risk_score != 8.0:
                arguments["riskScore"] = risk_score
            if additional_filter:
                arguments["additionalFilter"] = additional_filter
            if max_vulnerabilities != 25:
                arguments["maxVulnerabilitiesToDisplay"] = max_vulnerabilities
            
            result = run_async(MCPClient.call_tool("list_vulnerabilities", arguments))
            
            # Parse and format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
            
            return str(result)
            
        except Exception as e:
            return f"Error listing vulnerabilities: {str(e)}"


# ============================================================================
# LOG AND DATA QUERY TOOLS
# ============================================================================

class ExecuteDQLTool(BaseTool):
    name: str = "Execute DQL Query"
    description: str = (
        "Execute a Dynatrace Query Language (DQL) query to fetch logs, events, spans, or metrics. "
        "Use this for custom queries to analyze specific data. "
        "Input should be a valid DQL query string. "
        "Example: 'fetch logs | filter status == \"ERROR\" | limit 10'"
    )
    
    def _run(self, dql_statement: str, timeframe: str = "") -> str:
        """Execute DQL query"""
        try:
            arguments = {"dqlStatement": dql_statement}
            if timeframe:
                arguments["timeframe"] = timeframe
            
            result = run_async(MCPClient.call_tool("execute_dql", arguments))
            
            # Parse and format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
            
            return str(result)
            
        except Exception as e:
            return f"Error executing DQL: {str(e)}"


class GenerateDQLTool(BaseTool):
    name: str = "Generate DQL from Natural Language"
    description: str = (
        "Convert natural language queries to Dynatrace Query Language (DQL) using Davis CoPilot AI. "
        "Use this when you need to create a DQL query but don't know the exact syntax. "
        "Example: 'Show me error logs from the payment service in the last hour'"
    )
    
    def _run(self, natural_language_query: str, context: str = "") -> str:
        """Generate DQL from natural language"""
        try:
            arguments = {"naturalLanguageQuery": natural_language_query}
            if context:
                arguments["context"] = context
            
            result = run_async(MCPClient.call_tool("generate_dql_from_natural_language", arguments))
            
            # Parse and format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
            
            return str(result)
            
        except Exception as e:
            return f"Error generating DQL: {str(e)}"


# ============================================================================
# ENTITY DISCOVERY TOOLS
# ============================================================================

class FindEntityByNameTool(BaseTool):
    name: str = "Find Entity by Name"
    description: str = (
        "Find the entityId and type of a monitored entity (service, host, process-group, "
        "application, kubernetes-node, etc.) based on name. "
        "Use this to discover entity IDs before querying logs or metrics for specific entities."
    )
    
    def _run(self, entity_name: str) -> str:
        """Find entity by name"""
        try:
            arguments = {"entityName": entity_name}
            
            result = run_async(MCPClient.call_tool("find_entity_by_name", arguments))
            
            # Parse and format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
            
            return str(result)
            
        except Exception as e:
            return f"Error finding entity: {str(e)}"


# ============================================================================
# AI-POWERED ASSISTANCE TOOLS
# ============================================================================

class ChatWithDavisCopilotTool(BaseTool):
    name: str = "Chat with Davis CoPilot"
    description: str = (
        "Ask any Dynatrace-related question using Davis CoPilot AI. "
        "Use this for general guidance, best practices, or when no other specific tool is available. "
        "Example: 'How can I investigate slow database queries in Dynatrace?'"
    )
    
    def _run(self, message: str, context: str = "") -> str:
        """Chat with Davis CoPilot"""
        try:
            arguments = {"message": message}
            if context:
                arguments["context"] = context
            
            result = run_async(MCPClient.call_tool("chat_with_davis_copilot", arguments))
            
            # Parse and format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
            
            return str(result)
            
        except Exception as e:
            return f"Error chatting with Davis CoPilot: {str(e)}"


# ============================================================================
# UTILITY TOOLS
# ============================================================================

class GetEnvironmentInfoTool(BaseTool):
    name: str = "Get Dynatrace Environment Info"
    description: str = (
        "Get information about the connected Dynatrace Environment and verify the connection. "
        "Use this to confirm connectivity before running other queries."
    )
    
    def _run(self) -> str:
        """Get environment info"""
        try:
            result = run_async(MCPClient.call_tool("get_environment_info", {}))
            
            # Parse and format the result
            if hasattr(result, 'content'):
                content = result.content
                if isinstance(content, list) and len(content) > 0:
                    return content[0].text if hasattr(content[0], 'text') else str(content[0])
            
            return str(result)
            
        except Exception as e:
            return f"Error getting environment info: {str(e)}"


# Export all tools
__all__ = [
    'ListProblemsTool',
    'ListVulnerabilitiesTool',
    'ExecuteDQLTool',
    'GenerateDQLTool',
    'FindEntityByNameTool',
    'ChatWithDavisCopilotTool',
    'GetEnvironmentInfoTool'
]
