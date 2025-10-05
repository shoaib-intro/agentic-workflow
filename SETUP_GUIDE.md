# Setup Guide - Dynatrace Observability Multi-Agent System

This guide will walk you through setting up the multi-agent system step by step.

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.9 or higher installed
- [ ] pip (Python package manager)
- [ ] Node.js and npm installed
- [ ] Access to a Dynatrace environment
- [ ] OpenAI API account

## 🔧 Step-by-Step Setup

### Step 1: Verify Python Installation

```bash
python --version
# Should show Python 3.9 or higher
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Verify Node.js Installation

```bash
node --version
npm --version
```

If Node.js is not installed, download from [nodejs.org](https://nodejs.org/)

### Step 3: Install Python Dependencies

Navigate to the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- CrewAI (multi-agent framework)
- LangChain (LLM orchestration)
- OpenAI integration
- Rich (terminal UI)
- Requests (HTTP client)
- Other dependencies

### Step 4: Install Dynatrace MCP Server

Install the Dynatrace MCP Server globally:

```bash
npm install -g @dynatrace-oss/dynatrace-mcp-server
```

Verify installation:

```bash
npx @dynatrace-oss/dynatrace-mcp-server --version
```

### Step 5: Create Dynatrace Platform Token

1. **Log in to your Dynatrace environment**
   - Navigate to `https://your-env.apps.dynatrace.com`

2. **Go to Access Tokens**
   - Click on your profile (top right)
   - Select "Access tokens"
   - Click "Generate new token"

3. **Configure Token Scopes**
   
   Give your token a name (e.g., "MCP Multi-Agent System") and select these scopes:
   
   **Essential Scopes:**
   - ✅ `app-engine:apps:run`
   - ✅ `app-engine:functions:run`
   - ✅ `storage:buckets:read`
   - ✅ `storage:logs:read`
   - ✅ `storage:metrics:read`
   - ✅ `storage:spans:read`
   - ✅ `storage:events:read`
   - ✅ `storage:entities:read`
   - ✅ `storage:security.events:read`
   - ✅ `storage:system:read`
   
   **Optional (for enhanced features):**
   - `automation:workflows:read`
   - `automation:workflows:write`
   - `davis-copilot:conversations:execute`
   - `davis-copilot:nl2dql:execute`

4. **Generate and Copy Token**
   - Click "Generate token"
   - **IMPORTANT:** Copy the token immediately (it won't be shown again)
   - Token format: `dt0s16.XXXXXXXX.YYYYYYYY`

### Step 6: Get OpenAI API Key

1. **Visit OpenAI Platform**
   - Go to [platform.openai.com](https://platform.openai.com/)
   - Sign in or create an account

2. **Create API Key**
   - Navigate to API Keys section
   - Click "Create new secret key"
   - Give it a name (e.g., "Dynatrace Agent System")
   - Copy the key (format: `sk-...`)

3. **Add Credits (if needed)**
   - Ensure your OpenAI account has credits
   - The system uses GPT-4o-mini (cost-efficient)

### Step 7: Configure Environment Variables

1. **Copy the example environment file:**

```bash
cp .env.example .env
```

2. **Edit the .env file:**

```env
# Dynatrace Configuration
DT_ENVIRONMENT=https://abc12345.apps.dynatrace.com
DT_PLATFORM_TOKEN=dt0s16.SAMPLE.abcd1234
DT_GRAIL_QUERY_BUDGET_GB=1000

# OpenAI Configuration
OPENAI_API_KEY=sk-your-actual-key-here

# Agent Configuration
MAX_ITERATIONS=15
AGENT_VERBOSE=true
```

3. **Replace with your actual values:**
   - `DT_ENVIRONMENT`: Your Dynatrace environment URL
   - `DT_PLATFORM_TOKEN`: The token you created in Step 5
   - `OPENAI_API_KEY`: The API key from Step 6

### Step 8: Test Configuration

Run a quick test to verify everything is set up correctly:

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('DT_ENVIRONMENT:', os.getenv('DT_ENVIRONMENT')); print('Token configured:', 'Yes' if os.getenv('DT_PLATFORM_TOKEN') else 'No'); print('OpenAI configured:', 'Yes' if os.getenv('OPENAI_API_KEY') else 'No')"
```

You should see:
```
DT_ENVIRONMENT: https://your-env.apps.dynatrace.com
Token configured: Yes
OpenAI configured: Yes
```

### Step 9: Run the System

Start the multi-agent analysis:

```bash
python main.py
```

The system will:
1. Validate your configuration
2. Initialize all agents
3. Execute the analysis workflow
4. Generate reports

## 🎯 First Run Checklist

When you run the system for the first time:

- [ ] System displays welcome message
- [ ] Configuration is validated successfully
- [ ] All 5 agents are created
- [ ] All 5 tasks are defined
- [ ] Crew initialization completes
- [ ] Agents start working (you'll see progress)
- [ ] Analysis completes without errors
- [ ] Report is generated in `reports/` directory

## 🐛 Common Issues and Solutions

### Issue 1: "Module not found" Error

**Problem:** Python can't find installed packages

**Solution:**
```bash
# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Issue 2: "DT_ENVIRONMENT must be set"

**Problem:** Environment variables not loaded

**Solution:**
- Ensure `.env` file exists in the project root
- Check that `.env` contains all required variables
- Verify no extra spaces around `=` signs

### Issue 3: "403 Forbidden" from Dynatrace

**Problem:** Token doesn't have required scopes

**Solution:**
- Go back to Dynatrace and edit your token
- Add all required scopes listed in Step 5
- Generate a new token if needed
- Update `.env` with the new token

### Issue 4: OpenAI Rate Limit Error

**Problem:** Too many requests to OpenAI

**Solution:**
- Wait a few minutes and try again
- Check your OpenAI account has available credits
- Consider upgrading your OpenAI plan

### Issue 5: "No problems found"

**Problem:** Analysis returns no data

**Solution:**
- This is normal if your environment is healthy!
- Try extending the time range in `src/agents/tasks.py`
- Check a different Dynatrace environment with known issues
- Verify your token has access to the environment

## 📊 Verifying Successful Setup

After running the system, you should see:

1. **Console Output:**
   - Agent initialization messages
   - Task execution progress
   - Analysis completion message

2. **Generated Files:**
   - `reports/observability_report_*.md` (Markdown report)
   - `reports/observability_report_*.json` (JSON data)

3. **Report Contents:**
   - Executive summary
   - Problem analysis (if problems exist)
   - Security analysis (if vulnerabilities exist)
   - Log analysis
   - Synthesis and recommendations
   - Onboarding guide

## 🎓 Next Steps

Once setup is complete:

1. **Review the generated report** in the `reports/` directory
2. **Experiment with different time ranges** in task definitions
3. **Add custom tools** for specific Dynatrace features
4. **Modify agent behaviors** to focus on your use cases
5. **Integrate with your workflows** (CI/CD, Slack, etc.)

## 💡 Tips for Workshop

- **Start with a test environment** that has some problems/vulnerabilities
- **Monitor Grail usage** to understand cost implications
- **Experiment with agent prompts** to improve output quality
- **Share findings** with your team to demonstrate value

## 📞 Getting Help

If you encounter issues:

1. Check the troubleshooting section in README.md
2. Review Dynatrace MCP Server documentation
3. Check CrewAI documentation
4. Open an issue on GitHub (if applicable)

---

**You're all set! Run `python main.py` to start analyzing your Dynatrace environment.**
