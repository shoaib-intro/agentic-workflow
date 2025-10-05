# Running the Dynatrace Multi-Agent System

## ✅ System Overview

Your multi-agent system now uses the **Dynatrace MCP Server** to collect observability data. The system includes:

### 🤖 Agents:
1. **Problem Analyst** - Finds and analyzes open problems
2. **Security Analyst** - Identifies vulnerabilities and security risks
3. **Log Analyst** - Analyzes logs and correlates with issues
4. **Insights Synthesizer** - Creates comprehensive actionable reports
5. **Onboarding Guide** - Educates application owners

### 🛠️ MCP Tools (via Dynatrace MCP Server):
1. **ListProblemsTool** - List all open problems
2. **ListVulnerabilitiesTool** - List security vulnerabilities
3. **ExecuteDQLTool** - Execute DQL queries for logs/events
4. **FindEntityByNameTool** - Discover entity IDs
5. **GetEnvironmentInfoTool** - Verify Dynatrace connection
6. **GenerateDQLTool** - Generate DQL from natural language

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure you have:
- `mcp` library for MCP client
- `crewai` for multi-agent framework
- `langchain-openai` for LLM integration

### Step 2: Configure Environment

Ensure your `.env` file has:

```env
# Dynatrace
DT_ENVIRONMENT=https://fcy32356.live.dynatrace.com
DT_PLATFORM_TOKEN=your_token_here

# OpenAI
OPENAI_API_KEY=your_openai_key_here

# Optional
DT_GRAIL_QUERY_BUDGET_GB=1000
MAX_ITERATIONS=15
AGENT_VERBOSE=true
```

### Step 3: Test MCP Tools

Before running the full system, test that MCP tools work:

```bash
python test_mcp_tools.py
```

This will test:
- ✅ Connection to Dynatrace MCP Server
- ✅ Environment info retrieval
- ✅ Problem listing
- ✅ Vulnerability listing

### Step 4: Run the Multi-Agent System

```bash
python main.py
```

---

## 📊 What the System Does

### Use Case: Find Problems, Vulnerabilities, and Related Logs

1. **Problem Analyst Agent**:
   - Calls `ListProblemsTool` to get all open problems
   - Analyzes severity, impact, and affected entities
   - Prioritizes by business impact

2. **Security Analyst Agent**:
   - Calls `ListVulnerabilitiesTool` to get vulnerabilities
   - Assesses risk levels and CVEs
   - Provides remediation guidance

3. **Log Analyst Agent**:
   - Uses `GenerateDQLTool` to create DQL queries
   - Calls `ExecuteDQLTool` to fetch relevant logs
   - Uses `FindEntityByNameTool` to discover entities
   - Correlates logs with problems and vulnerabilities

4. **Insights Synthesizer Agent**:
   - Combines all findings
   - Creates prioritized recommendations
   - Provides actionable mitigation steps

5. **Onboarding Guide Agent**:
   - Explains Dynatrace capabilities
   - Provides practical examples
   - Guides next steps

---

## 🔧 Troubleshooting

### Issue: "MCP library not installed"
```bash
pip install mcp
```

### Issue: "Error connecting to MCP server"
**Check:**
1. Node.js and npm are installed: `node --version`
2. MCP server package is accessible: `npx -y @dynatrace-oss/dynatrace-mcp-server@latest --version`
3. Environment variables are set correctly in `.env`

### Issue: "401 Unauthorized" or "404 Not Found"
**Solution:**
- Verify `DT_ENVIRONMENT` URL is correct (use `.live.dynatrace.com` format)
- Check `DT_PLATFORM_TOKEN` is valid and not expired
- Ensure token has required scopes (see below)

### Issue: Agents timeout or hang
**Solution:**
- Reduce `MAX_ITERATIONS` in `.env` to 10
- Reduce time ranges in task descriptions
- Check network connectivity to Dynatrace

---

## 🔐 Required Token Scopes

Your Dynatrace platform token needs these scopes:

**Essential:**
- `app-engine:apps:run`
- `app-engine:functions:run`
- `storage:buckets:read`
- `storage:logs:read`
- `storage:events:read`
- `storage:security.events:read`

**Optional (for enhanced features):**
- `davis-copilot:conversations:execute`
- `davis-copilot:nl2dql:execute`
- `automation:workflows:read`

---

## 📈 Expected Output

The system will generate:

1. **Console Output**: Real-time agent progress and decisions
2. **Final Report**: Comprehensive analysis with:
   - Executive summary
   - Prioritized issues
   - Detailed analysis with evidence
   - Actionable recommendations
   - Onboarding guidance

3. **Report Files** (in `reports/` directory):
   - `observability_report_*.md` - Markdown format
   - `observability_report_*.json` - JSON format

---

## 💰 Cost Considerations

### Dynatrace Costs:
- Grail queries: ~1-5 GB per analysis
- Cost: ~$0.0035-$0.0175 per analysis
- Budget tracked via `DT_GRAIL_QUERY_BUDGET_GB`

### OpenAI Costs:
- Model: GPT-4o-mini (cost-efficient)
- Tokens: ~10,000-50,000 per analysis
- Cost: ~$0.01 per analysis

**Total: ~$0.02 per analysis**

---

## 🎯 Customization

### Adjust Time Ranges

Edit `src/agents/tasks.py`:

```python
# For problems (default: 24 hours)
"Analyze all open problems in Dynatrace for the last 24 hours."

# For vulnerabilities (default: 30 days via MCP server)
# Controlled by MCP server, returns last 30 days

# For logs (default: 6 hours)
"Query error logs from the last 6 hours"
```

### Add More Tools

The MCP server provides 16 tools total. Currently using 6. You can add:
- `chat_with_davis_copilot` - AI-powered assistance
- `send_email` - Email notifications
- `get_kubernetes_events` - K8s cluster events
- And more...

See `get_mcp_tools.py` output for full list.

---

## 📚 Additional Scripts

### List All MCP Tools
```bash
python get_mcp_tools.py
```
Shows all 16 available tools from the MCP server with parameters.

### Test Individual Tools
```bash
python test_mcp_tools.py
```
Tests each tool individually to verify they work.

---

## ✅ Success Checklist

Before running `main.py`, ensure:

- [ ] Python 3.9+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with valid credentials
- [ ] Node.js and npm installed
- [ ] MCP server accessible (`npx -y @dynatrace-oss/dynatrace-mcp-server@latest`)
- [ ] Test tools pass (`python test_mcp_tools.py`)
- [ ] OpenAI API key is valid and has credits

---

## 🎓 For Workshop Presentation

### Key Points to Highlight:

1. **Hierarchical Architecture**: Specialist agents + master synthesizer
2. **MCP Integration**: Using Dynatrace MCP Server for data access
3. **Real-time Analysis**: Actual data from your Dynatrace environment
4. **Actionable Insights**: Prioritized recommendations, not just raw data
5. **Educational Component**: Onboarding guide for new users

### Demo Flow:

1. Show the architecture diagram
2. Explain each agent's role
3. Run `python test_mcp_tools.py` to show MCP integration
4. Run `python main.py` to show full system
5. Walk through the generated report
6. Discuss extensibility and customization

---

## 🆘 Getting Help

If you encounter issues:

1. Check this README
2. Run `python test_mcp_tools.py` to isolate issues
3. Review error messages carefully
4. Check Dynatrace token scopes
5. Verify network connectivity

---

**You're all set! Run `python main.py` to start the analysis.** 🚀
