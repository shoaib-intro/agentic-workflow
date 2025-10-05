# 🚀 START HERE - Quick Start Guide

## Welcome to the Dynatrace Observability Multi-Agent System!

This is your **one-page guide** to get started immediately.

---

## ⚡ 3-Step Quick Start

### Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment (2 minutes)

Make sure your `.env` file has:

```env
DT_ENVIRONMENT=https://fcy32356.live.dynatrace.com
DT_PLATFORM_TOKEN=your_token_here
OPENAI_API_KEY=your_openai_key_here
```

### Step 3: Run the System (3 minutes)

```bash
python main.py
```

**That's it!** The system will analyze your Dynatrace environment and generate a comprehensive report.

---

## 🧪 Before Running - Test First

### Test MCP Tools Work:

```bash
python test_mcp_tools.py
```

**Expected output:**
```
✅ Success! GetEnvironmentInfoTool
✅ Success! ListProblemsTool
✅ Success! ListVulnerabilitiesTool
```

If all tests pass, you're ready to run the full system!

---

## 📊 What You'll Get

After running `python main.py`, you'll receive:

1. **Console Output** - Real-time agent progress
2. **Comprehensive Report** - Saved in `reports/` directory
3. **JSON Data** - Machine-readable results

### Report Includes:
- ✅ All open problems (last 12 hours)
- ✅ Security vulnerabilities (last 30 days)
- ✅ Related error logs
- ✅ Correlation insights
- ✅ Prioritized recommendations
- ✅ Onboarding guide for Dynatrace

---

## 🎯 Use Case Solved

**Task:** Find open problems or vulnerabilities and related logs, present them in an actionable manner.

**Solution:**
1. **Problem Analyst** finds all open problems via MCP
2. **Security Analyst** identifies vulnerabilities via MCP
3. **Log Analyst** queries related logs via DQL
4. **Synthesizer** creates actionable report
5. **Guide** educates on using Dynatrace

**Result:** Comprehensive, prioritized, actionable insights in 3 minutes!

---

## 🔧 Troubleshooting

### Issue: "MCP library not installed"
```bash
pip install mcp
```

### Issue: "Error connecting to MCP server"
- Check Node.js is installed: `node --version`
- Verify `.env` has correct credentials
- Use `.live.dynatrace.com` URL format

### Issue: "No problems found"
- This is good! Your system is healthy
- Try extending time range or different environment

---

## 📚 Need More Help?

- **Setup Issues?** → Read `SETUP_GUIDE.md`
- **Understanding Architecture?** → Read `ARCHITECTURE.md`
- **Running System?** → Read `RUN_INSTRUCTIONS.md`
- **Workshop Prep?** → Read `WORKSHOP_GUIDE.md`
- **Quick Reference?** → Read `QUICK_REFERENCE.md`

---

## 🎓 For Workshop (40 minutes)

### Presentation Flow:

1. **Intro** (5 min) - Problem statement and solution
2. **Architecture** (10 min) - Show hierarchical design
3. **Live Demo** (15 min) - Run the system live
4. **Use Case** (5 min) - Walk through generated report
5. **Technical** (5 min) - MCP integration highlights

### Demo Commands:

```bash
# Show MCP tools
python get_mcp_tools.py

# Test tools
python test_mcp_tools.py

# Run full system
python main.py
```

---

## ✅ Pre-Flight Checklist

Before your presentation:

- [ ] All dependencies installed
- [ ] `.env` configured with valid credentials
- [ ] `python test_mcp_tools.py` passes
- [ ] `python main.py` runs successfully
- [ ] Report generated in `reports/` directory
- [ ] Reviewed generated report
- [ ] Prepared to explain architecture
- [ ] Ready to discuss extensions

---

## 🎯 Key Selling Points

1. **Automated Analysis** - 3 minutes vs. 2-4 hours manual
2. **MCP Integration** - Uses official Dynatrace MCP Server
3. **Hierarchical AI** - Specialist agents + master synthesizer
4. **Actionable Insights** - Not just data, but recommendations
5. **Educational** - Helps users understand Dynatrace
6. **Cost-Effective** - ~$0.02 per analysis
7. **Extensible** - 10 more MCP tools available
8. **Production-Ready** - Error handling, logging, reports

---

## 🚀 You're Ready!

Everything is set up and ready to go. Just run:

```bash
python main.py
```

**Good luck with your workshop presentation!** 🎉

---

**Questions? Check the comprehensive documentation in this directory.**
