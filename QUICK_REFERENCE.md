# Quick Reference Guide

## 🚀 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the system
python main.py
```

## 📁 Project Structure

```
DT workshop/
├── main.py                          # Entry point
├── requirements.txt                 # Dependencies
├── .env                            # Configuration (create from .env.example)
├── src/
│   ├── crew_orchestrator.py        # Main orchestration
│   ├── agents/
│   │   ├── specialist_agents.py    # Agent definitions
│   │   └── tasks.py                # Task definitions
│   └── tools/
│       └── dynatrace_mcp_tools.py  # Dynatrace tools
└── reports/                         # Generated reports
```

## 🔑 Required Environment Variables

```env
# Dynatrace
DT_ENVIRONMENT=https://your-env.apps.dynatrace.com
DT_PLATFORM_TOKEN=dt0s16.YOUR_TOKEN
DT_GRAIL_QUERY_BUDGET_GB=1000

# OpenAI
OPENAI_API_KEY=sk-your-key-here
```

## 🛠️ Dynatrace Token Scopes

**Essential:**
- `app-engine:apps:run`
- `app-engine:functions:run`
- `storage:buckets:read`
- `storage:logs:read`
- `storage:metrics:read`
- `storage:spans:read`
- `storage:events:read`
- `storage:entities:read`
- `storage:security.events:read`

**Optional:**
- `davis-copilot:conversations:execute`
- `automation:workflows:read`

## 🤖 Agent Overview

| Agent | Role | Tools | Output |
|-------|------|-------|--------|
| Problem Analyst | Identifies problems | GetProblems, GetProblemDetails | Problem report |
| Security Analyst | Finds vulnerabilities | GetSecurityProblems | Security report |
| Log Analyst | Analyzes logs | ExecuteDQL, GetLogsForEntity | Log analysis |
| Insights Synthesizer | Synthesizes findings | None | Comprehensive report |
| Onboarding Guide | Creates guide | None | Onboarding documentation |

## 📊 Typical Workflow

```
1. Problem Analyst → Identifies 3 problems
2. Security Analyst → Finds 2 vulnerabilities
3. Log Analyst → Correlates logs (uses context from 1 & 2)
4. Synthesizer → Creates comprehensive report (uses all context)
5. Onboarding Guide → Generates educational content (uses synthesis)
```

## 🔧 Common Customizations

### Change Time Ranges

Edit `src/agents/tasks.py`:

```python
# Problems (default: 24 hours)
"Analyze all open problems in Dynatrace for the last 24 hours."
# Change to: "for the last 48 hours."

# Security (default: 7 days)
"Analyze security problems and vulnerabilities in Dynatrace for the last 7 days."
# Change to: "for the last 14 days."

# Logs (default: 6 hours)
"Query error logs from the last 6 hours"
# Change to: "from the last 12 hours"
```

### Adjust Agent Temperature

Edit `src/agents/specialist_agents.py`:

```python
# More creative (0.7-1.0)
llm=create_llm(temperature=0.8)

# More precise (0.1-0.3)
llm=create_llm(temperature=0.2)

# Balanced (0.4-0.6)
llm=create_llm(temperature=0.5)
```

### Add Custom Tool

In `src/tools/dynatrace_mcp_tools.py`:

```python
class MyCustomTool(BaseTool):
    name: str = "My Tool Name"
    description: str = "What it does"
    
    def _run(self, input: str) -> str:
        client = DynatraceClient()
        # Your logic here
        return "Result"
```

## 📈 Cost Estimates

### Dynatrace Grail
- **Typical analysis:** 1-5 GB scanned
- **Cost:** ~$0.0035-$0.0175 per analysis
- **Budget:** Configurable via `DT_GRAIL_QUERY_BUDGET_GB`

### OpenAI
- **Model:** GPT-4o-mini
- **Tokens:** ~10,000-50,000 per analysis
- **Cost:** ~$0.01 per analysis

**Total:** ~$0.02 per analysis

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "DT_ENVIRONMENT must be set" | Check `.env` file exists and is configured |
| "403 Forbidden" | Add required scopes to Dynatrace token |
| "No problems found" | Normal if environment is healthy; try different time range |
| Agent timeout | Increase `max_iter` in agent config or reduce time ranges |
| OpenAI rate limit | Wait and retry; check account credits |

## 📝 DQL Query Examples

### Get Error Logs
```dql
fetch logs
| filter status == "ERROR"
| sort timestamp desc
| limit 50
```

### Get Logs for Specific Service
```dql
fetch logs
| filter dt.source_entity == "SERVICE-123"
| fields timestamp, status, content
| limit 100
```

### Count Errors by Service
```dql
fetch logs
| filter status == "ERROR"
| summarize count(), by: {dt.source_entity}
| sort count() desc
```

### Get Slow Queries
```dql
fetch logs
| filter contains(content, "SlowQuery")
| fields timestamp, content
| limit 50
```

## 🎯 Best Practices

### For Development
- Use virtual environment: `python -m venv venv`
- Test with small time ranges first
- Monitor Grail budget usage
- Keep tokens secure (never commit `.env`)

### For Production
- Set appropriate budget limits
- Schedule regular analyses (daily/weekly)
- Integrate with alerting systems
- Archive reports for historical analysis
- Monitor system costs

### For Workshop
- Prepare test environment with problems
- Have backup screenshots ready
- Test all commands beforehand
- Keep examples relevant to audience
- Encourage hands-on experimentation

## 📚 Useful Links

- [Dynatrace MCP Server](https://github.com/dynatrace-oss/dynatrace-mcp)
- [CrewAI Docs](https://docs.crewai.com/)
- [DQL Reference](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-query-language)
- [Dynatrace API](https://docs.dynatrace.com/docs/dynatrace-api)

## 🔍 Verification Checklist

Before running:
- [ ] Python 3.9+ installed
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Dynatrace token has required scopes
- [ ] OpenAI API key is valid
- [ ] Network access to Dynatrace environment

After running:
- [ ] No errors in console output
- [ ] Report generated in `reports/` directory
- [ ] Report contains expected sections
- [ ] JSON file also created
- [ ] Findings are relevant to your environment

## 💡 Pro Tips

1. **Start Small:** Begin with shorter time ranges to minimize costs
2. **Iterate:** Run multiple times with different configurations
3. **Customize:** Adjust agent prompts for your specific needs
4. **Monitor:** Track Grail usage to understand cost patterns
5. **Automate:** Schedule regular analyses for continuous monitoring
6. **Share:** Export reports and share with stakeholders
7. **Learn:** Review agent outputs to understand analysis patterns
8. **Extend:** Add custom tools for your specific use cases

## 🆘 Getting Help

1. Check `SETUP_GUIDE.md` for detailed setup instructions
2. Review `ARCHITECTURE.md` for system design details
3. See `WORKSHOP_GUIDE.md` for presentation tips
4. Check `example_output.md` for expected results
5. Review troubleshooting section in `README.md`

---

**Quick Reference Version 1.0 - Updated 2025-10-05**
