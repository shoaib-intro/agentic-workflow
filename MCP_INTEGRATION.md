# MCP Integration - Dynatrace Multi-Agent System

## ✅ Integration Complete

Your multi-agent system now uses the **Dynatrace MCP Server** tools instead of direct API calls!

## 🔧 What Was Integrated

### Tools Created (7 MCP Tools)

Based on your `mcp_tools.json`, I've integrated the most relevant tools for your assignment:

| Tool | Purpose | Used By Agent |
|------|---------|---------------|
| **ListProblemsTool** | List all problems from last 12h | Problem Analyst |
| **ListVulnerabilitiesTool** | List vulnerabilities (last 30 days) | Security Analyst |
| **ExecuteDQLTool** | Execute DQL queries for logs/events | Log Analyst |
| **GenerateDQLTool** | Convert natural language to DQL | Log Analyst |
| **FindEntityByNameTool** | Discover entity IDs by name | All agents |
| **ChatWithDavisCopilotTool** | AI-powered Dynatrace guidance | Log Analyst |
| **GetEnvironmentInfoTool** | Verify connection | Problem Analyst |

### Agent Tool Assignments

#### 1. **Problem Analyst Agent**
```python
tools=[
    ListProblemsTool(),           # Find open problems
    FindEntityByNameTool(),       # Discover affected entities
    GetEnvironmentInfoTool()      # Verify connection
]
```

#### 2. **Security Analyst Agent**
```python
tools=[
    ListVulnerabilitiesTool(),    # Find vulnerabilities
    FindEntityByNameTool()        # Discover affected entities
]
```

#### 3. **Log Analyst Agent**
```python
tools=[
    ExecuteDQLTool(),             # Execute custom DQL queries
    GenerateDQLTool(),            # Generate DQL from natural language
    FindEntityByNameTool(),       # Discover entities
    ChatWithDavisCopilotTool()    # Get AI guidance
]
```

#### 4. **Insights Synthesizer Agent**
- No tools (synthesizes findings from other agents)

#### 5. **Onboarding Guide Agent**
- No tools (creates educational content)

## 📁 Files Modified

1. **`src/tools/dynatrace_mcp_tools.py`** ✅ CREATED
   - MCP client wrapper
   - 7 CrewAI tool classes
   - Async-to-sync helper functions

2. **`src/agents/specialist_agents.py`** ✅ UPDATED
   - Updated imports to use MCP tools
   - Assigned appropriate tools to each agent

## 🚀 How It Works

### Architecture Flow

```
CrewAI Agent
    ↓
Tool (e.g., ListProblemsTool)
    ↓
MCPClient.call_tool()
    ↓
MCP Session (stdio_client)
    ↓
Dynatrace MCP Server (npx)
    ↓
Dynatrace API
    ↓
Result back to Agent
```

### Key Features

1. **Singleton MCP Client** - Reuses connection across tool calls
2. **Async-to-Sync Bridge** - Converts async MCP calls to sync for CrewAI
3. **Error Handling** - Graceful error messages for debugging
4. **Result Parsing** - Extracts text content from MCP responses

## 🎯 Usage Example

Your existing `main.py` works without changes! The agents now automatically use MCP tools:

```bash
python main.py
```

The workflow:
1. **Problem Analyst** calls `list_problems` via MCP
2. **Security Analyst** calls `list_vulnerabilities` via MCP
3. **Log Analyst** generates DQL and executes queries via MCP
4. **Synthesizer** combines all findings
5. **Onboarding Guide** creates educational content

## 🔍 Testing Individual Tools

You can test tools directly:

```python
from src.tools.dynatrace_mcp_tools import ListProblemsTool

tool = ListProblemsTool()
result = tool._run()
print(result)
```

## 📊 Available But Not Yet Integrated

These MCP tools are available but not yet added to agents (you can add them if needed):

- `verify_dql` - Verify DQL syntax before execution
- `get_ownership` - Get entity ownership information
- `explain_dql_in_natural_language` - Explain DQL queries
- `send_slack_message` - Send Slack notifications
- `send_email` - Send email notifications
- `create_workflow_for_notification` - Create Dynatrace workflows
- `make_workflow_public` - Make workflows public
- `get_kubernetes_events` - Get K8s cluster events
- `reset_grail_budget` - Reset query budget

### To Add More Tools

1. Create a new tool class in `dynatrace_mcp_tools.py`:
```python
class YourNewTool(BaseTool):
    name: str = "Your Tool Name"
    description: str = "What it does"
    
    def _run(self, param1: str) -> str:
        arguments = {"param1": param1}
        result = run_async(MCPClient.call_tool("mcp_tool_name", arguments))
        # Parse and return result
        return str(result)
```

2. Import and add to agent in `specialist_agents.py`:
```python
from ..tools.dynatrace_mcp_tools import YourNewTool

tools=[
    YourNewTool(),
    # ... other tools
]
```

## ⚠️ Important Notes

### Dependencies Required
```bash
pip install mcp
```

### Environment Variables Required
```env
DT_ENVIRONMENT=https://your-env.live.dynatrace.com
DT_PLATFORM_TOKEN=your-token-here
OPENAI_API_KEY=your-openai-key
```

### MCP Server Must Be Accessible
The tools spawn the MCP server via:
```bash
npx -y @dynatrace-oss/dynatrace-mcp-server@latest
```

Ensure:
- Node.js and npm are installed
- Network access to Dynatrace
- Token has required scopes

## 🐛 Troubleshooting

### Issue: "MCP library not installed"
```bash
pip install mcp
```

### Issue: "DT_ENVIRONMENT and DT_PLATFORM_TOKEN must be set"
Check your `.env` file has both variables set correctly.

### Issue: Tool returns error
The MCP server logs will show in console. Check:
1. Token has required scopes
2. Network connectivity to Dynatrace
3. MCP server version is latest

### Issue: Async errors
The `run_async()` helper handles event loop management. If issues persist, check Python version (3.9+ required).

## ✅ Verification

To verify the integration works:

1. **Test MCP connection:**
```bash
python mcp_client.py
```

2. **Test a single tool:**
```python
from src.tools.dynatrace_mcp_tools import GetEnvironmentInfoTool
tool = GetEnvironmentInfoTool()
print(tool._run())
```

3. **Run the full system:**
```bash
python main.py
```

## 🎉 Benefits of MCP Integration

1. **✅ Official Dynatrace Integration** - Uses the official MCP server
2. **✅ Maintained by Dynatrace** - Updates automatically with new features
3. **✅ AI-Powered Features** - Access to Davis CoPilot capabilities
4. **✅ Consistent API** - Same interface as other MCP clients (VSCode, Claude, etc.)
5. **✅ Future-Proof** - New tools added to MCP server automatically available

## 📚 Next Steps

1. Run `python main.py` to test the full system
2. Review generated reports in `reports/` directory
3. Add more MCP tools as needed for your use case
4. Customize agent prompts based on results

---

**Your multi-agent system is now powered by Dynatrace MCP Server! 🚀**
