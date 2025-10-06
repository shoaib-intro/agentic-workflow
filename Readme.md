# Dynatrace Observability Multi-Agent System

A sophisticated multi-agent system built with CrewAI that leverages the Dynatrace MCP Server to provide comprehensive observability insights for application owners.

## 🎯 Overview

This system uses a **hierarchical multi-agent architecture** where specialized AI agents collaborate to analyze Dynatrace observability data and deliver actionable insights. Each agent is an expert in their domain, working together to provide a complete picture of your application's health, security posture, and operational status.

## 🏗️ Architecture

### Hierarchical Agent Structure

```
┌─────────────────────────────────────────────────────────────┐
│                  Onboarding Guide Agent                      │
│            (Educational & Best Practices)                    │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌─────────────────────────────────────────────────────────────┐
│              Insights Synthesizer Agent                      │
│           (Master Agent - Orchestrates & Synthesizes)        │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────────────┐  ┌────────────────┐  ┌───────────────┐
│   Problem     │  │   Security     │  │     Log       │
│   Analyst     │  │   Analyst      │  │   Analyst     │
│   Agent       │  │   Agent        │  │   Agent       │
└───────────────┘  └────────────────┘  └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │  Dynatrace MCP Server │
                │  (Data Source)        │
                └───────────────────────┘
```

### Agent Roles

1. **Problem Analyst Agent** 🔍
   - Identifies and analyzes open problems and incidents
   - Assesses severity, impact, and affected entities
   - Provides root cause analysis when available
   - Prioritizes issues by business impact

2. **Security Analyst Agent** 🔒
   - Identifies security vulnerabilities and CVEs
   - Assesses risk levels and exposure
   - Tracks affected components and libraries
   - Provides remediation guidance

3. **Log Analyst Agent** 📊
   - Analyzes logs to find error patterns
   - Correlates log entries with problems and vulnerabilities
   - Extracts meaningful insights from log data
   - Supports root cause analysis with log evidence

4. **Insights Synthesizer Agent** 🧠
   - Master agent that synthesizes all findings
   - Creates comprehensive, actionable reports
   - Correlates data across all sources
   - Provides prioritized recommendations

5. **Onboarding Guide Agent** 📚
   - Educates application owners about Dynatrace
   - Explains available data types and their uses
   - Provides best practices and guidance
   - Creates practical, example-based documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Dynatrace environment with platform token
- OpenAI API key (for CrewAI agents)
- Node.js and npm (for Dynatrace MCP Server)

### Installation

1. **Clone or download this repository**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Dynatrace MCP Server**
   ```bash
   npm install -g @dynatrace-oss/dynatrace-mcp-server
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   DT_ENVIRONMENT=https://your-env.apps.dynatrace.com
   DT_PLATFORM_TOKEN=dt0s16.YOUR_TOKEN_HERE
   OPENAI_API_KEY=sk-your-openai-key-here
   ```

5. **Create required Dynatrace token scopes**
   
   Your platform token needs these scopes:
   - `app-engine:apps:run`
   - `app-engine:functions:run`
   - `storage:buckets:read`
   - `storage:logs:read`
   - `storage:metrics:read`
   - `storage:spans:read`
   - `storage:events:read`
   - `storage:entities:read`
   - `storage:security.events:read`

### Running the System

```bash
python main.py
```

The system will:
1. Validate your configuration
2. Initialize all agents
3. Execute the analysis workflow
4. Generate a comprehensive report
5. Save results to the `reports/` directory

## 📋 Use Case: Find Open Problems & Vulnerabilities

The system addresses the key use case of finding open problems or vulnerabilities and related logs, presenting them in an actionable manner:

### Workflow

1. **Problem Detection**
   - Scans for all open problems in the last 24 hours
   - Retrieves detailed information for each problem
   - Identifies affected entities and services

2. **Security Assessment**
   - Identifies vulnerabilities from the last 7 days
   - Assesses risk levels and CVE information
   - Determines exposure across the environment

3. **Log Correlation**
   - Analyzes error logs related to identified issues
   - Extracts relevant log entries for context
   - Identifies patterns and anomalies

4. **Synthesis & Reporting**
   - Combines all findings into a unified report
   - Prioritizes issues by severity and impact
   - Provides actionable mitigation steps
   - Correlates problems, vulnerabilities, and logs

5. **Educational Guidance**
   - Explains how to use Dynatrace data effectively
   - Provides best practices for monitoring
   - Guides application owners on next steps

## 📊 Output

The system generates two types of reports:

### 1. Markdown Report (`reports/observability_report_*.md`)
A human-readable report with:
- Executive summary
- Detailed analysis of each issue
- Prioritized recommendations
- Onboarding guidance

### 2. JSON Report (`reports/observability_report_*.json`)
Machine-readable data including:
- All raw findings
- Metadata and timestamps
- Execution details

## 🛠️ Customization

### Adjusting Time Ranges

Edit `src/agents/tasks.py` to modify time ranges:
```python
# For problems (default: 24 hours)
"Analyze all open problems in Dynatrace for the last 24 hours."

# For security (default: 7 days)
"Analyze security problems and vulnerabilities in Dynatrace for the last 7 days."

# For logs (default: 6 hours)
"Query error logs from the last 6 hours"
```

### Adding Custom Tools

Create new tools in `src/tools/dynatrace_mcp_tools.py`:
```python
class CustomTool(BaseTool):
    name: str = "Your Tool Name"
    description: str = "What your tool does"
    
    def _run(self, input: str) -> str:
        # Your implementation
        pass
```

### Modifying Agent Behavior

Edit agent configurations in `src/agents/specialist_agents.py`:
```python
def create_custom_agent() -> Agent:
    return Agent(
        role="Your Role",
        goal="Your Goal",
        backstory="Your Backstory",
        tools=[YourTools()],
        llm=create_llm(temperature=0.5)
    )
```

## 💰 Cost Considerations

### Dynatrace Costs
- Querying Dynatrace Grail incurs costs based on GB scanned
- Default budget: 1000 GB per session
- Adjust via `DT_GRAIL_QUERY_BUDGET_GB` environment variable
- Start with smaller time ranges to minimize costs

### OpenAI Costs
- Uses GPT-4o-mini for cost efficiency
- Typical analysis: ~10,000-50,000 tokens
- Estimated cost: $0.05-$0.25 per analysis

## 🔧 Troubleshooting

### Authentication Issues
```
Error: DT_ENVIRONMENT and DT_PLATFORM_TOKEN must be set
```
**Solution:** Ensure `.env` file exists with correct credentials

### Missing Scopes
```
Error: 403 Forbidden
```
**Solution:** Add required scopes to your Dynatrace platform token

### Agent Timeout
```
Error: Agent exceeded max iterations
```
**Solution:** Increase `max_iter` in agent configurations or reduce time ranges

### No Data Found
```
No open problems found in the specified time range
```
**Solution:** This is normal if your environment is healthy. Try extending the time range or checking a different environment.

## 📚 Project Structure

```
DT workshop/
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── README.md                        # This file
├── src/
│   ├── __init__.py
│   ├── crew_orchestrator.py        # Crew orchestration logic
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── specialist_agents.py    # Agent definitions
│   │   └── tasks.py                # Task definitions
│   └── tools/
│       ├── __init__.py
│       └── dynatrace_mcp_tools.py  # Dynatrace API tools
└── reports/                         # Generated reports
    └── .gitkeep
```

## 🎓 For Workshop Participants

### Key Concepts Demonstrated

1. **Multi-Agent Collaboration**: Specialized agents working together
2. **Hierarchical Architecture**: Master agent coordinating specialists
3. **Context Sharing**: Agents building on each other's findings
4. **Tool Integration**: Custom tools for Dynatrace API
5. **Sequential Workflow**: Structured, step-by-step analysis

### Discussion Points

- How does the hierarchical structure improve analysis quality?
- What are the benefits of specialized agents vs. a single agent?
- How can we extend this system for other use cases?
- What are the trade-offs between agent autonomy and coordination?
- How can we optimize for cost and performance?


## 📄 License

This project is provided as-is for Dynatrace workshop.

## 🔗 Resources

- [Dynatrace MCP Server](https://github.com/dynatrace-oss/dynatrace-mcp)
- [CrewAI Documentation](https://docs.crewai.com/)
- [Dynatrace API Documentation](https://docs.dynatrace.com/docs/dynatrace-api)
- [DQL Documentation](https://docs.dynatrace.com/docs/discover-dynatrace/references/dynatrace-query-language)

---

**Built with ❤️ using CrewAI and Dynatrace MCP Server**
