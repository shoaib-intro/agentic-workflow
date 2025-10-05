"""
Tasks for the Dynatrace Observability Multi-Agent System
Defines the workflow and responsibilities for each agent
"""

from crewai import Task
from typing import List


def create_problem_analysis_task(agent) -> Task:
    """Task for analyzing problems in Dynatrace"""
    return Task(
        description=(
            "Analyze all open problems in Dynatrace for the last 24 hours. "
            "For each problem found:\n"
            "1. Retrieve the problem details including severity, impact, and affected entities\n"
            "2. Identify the root cause if available\n"
            "3. Assess the business impact and urgency\n"
            "4. List all affected services and infrastructure components\n"
            "5. Note the timeline of the problem (when it started, duration)\n\n"
            "Provide a structured summary of all problems, prioritized by severity and impact. "
            "If no problems are found, clearly state that the system is healthy."
        ),
        expected_output=(
            "A detailed report containing:\n"
            "- Total number of open problems\n"
            "- For each problem: ID, title, severity, status, impact level, affected entities, "
            "root cause, start time, and recommended priority\n"
            "- Summary of most critical issues requiring immediate attention"
        ),
        agent=agent
    )


def create_security_analysis_task(agent) -> Task:
    """Task for analyzing security vulnerabilities"""
    return Task(
        description=(
            "Analyze security problems and vulnerabilities in Dynatrace for the last 7 days. "
            "For each security issue found:\n"
            "1. Identify the vulnerability (CVE ID if available)\n"
            "2. Assess the risk level and severity\n"
            "3. Identify affected components, libraries, or services\n"
            "4. Determine the exposure level (how many entities are affected)\n"
            "5. Check the status (open, resolved, muted)\n\n"
            "Provide a structured summary of all security issues, prioritized by risk level. "
            "If no vulnerabilities are found, clearly state that no security issues were detected."
        ),
        expected_output=(
            "A comprehensive security report containing:\n"
            "- Total number of security problems\n"
            "- For each vulnerability: ID, CVE, title, risk level, status, affected technology, "
            "number of affected entities, first seen date\n"
            "- Prioritized list of critical vulnerabilities requiring immediate remediation\n"
            "- Summary of overall security posture"
        ),
        agent=agent
    )


def create_log_analysis_task(agent, context: List[Task]) -> Task:
    """Task for analyzing logs related to problems and vulnerabilities"""
    return Task(
        description=(
            "Based on the problems and security issues identified by other agents, "
            "analyze relevant logs to provide additional context and insights. "
            "Your analysis should:\n"
            "1. Query error logs from the last 6 hours to identify patterns\n"
            "2. For each problem or affected entity mentioned in the context, "
            "retrieve and analyze relevant log entries\n"
            "3. Identify error patterns, stack traces, or anomalies in the logs\n"
            "4. Correlate log entries with the problems and vulnerabilities found\n"
            "5. Extract key error messages and their frequency\n\n"
            "Use DQL queries to fetch logs efficiently. Focus on ERROR and WARN level logs. "
            "If specific entities are mentioned in the context, prioritize logs from those entities."
        ),
        expected_output=(
            "A log analysis report containing:\n"
            "- Summary of error patterns found in logs\n"
            "- Key error messages and their frequency\n"
            "- Correlation between log entries and identified problems\n"
            "- Relevant log excerpts that provide context for issues\n"
            "- Any anomalies or unexpected patterns in the log data"
        ),
        agent=agent,
        context=context  # Receives context from previous tasks
    )


def create_synthesis_task(agent, context: List[Task]) -> Task:
    """Task for synthesizing all findings into actionable insights"""
    return Task(
        description=(
            "Synthesize all findings from the Problem Analyst, Security Analyst, and Log Analyst "
            "into a comprehensive, actionable report for application owners. Your report should:\n\n"
            "1. **Executive Summary**: Provide a high-level overview of the current state\n"
            "2. **Critical Issues**: List all critical problems and vulnerabilities requiring immediate action\n"
            "3. **Detailed Analysis**: For each issue, provide:\n"
            "   - Clear description of the problem\n"
            "   - Business impact and affected users/services\n"
            "   - Root cause analysis (if available)\n"
            "   - Supporting evidence from logs\n"
            "   - Recommended mitigation actions\n"
            "   - Priority level (Critical/High/Medium/Low)\n"
            "4. **Correlation Insights**: Show how problems, vulnerabilities, and logs are connected\n"
            "5. **Actionable Recommendations**: Provide specific, prioritized steps to resolve issues\n\n"
            "Present the information in a clear, structured format that non-technical stakeholders "
            "can understand and act upon. Use bullet points, clear headings, and prioritization."
        ),
        expected_output=(
            "A comprehensive observability report with:\n"
            "- Executive summary of system health\n"
            "- Prioritized list of issues with severity, impact, and recommendations\n"
            "- Detailed analysis of each critical issue with supporting evidence\n"
            "- Correlation between problems, vulnerabilities, and log patterns\n"
            "- Clear, actionable mitigation steps for each issue\n"
            "- Overall recommendations for improving system reliability and security"
        ),
        agent=agent,
        context=context  # Receives context from all previous tasks
    )


def create_onboarding_guide_task(agent, context: List[Task]) -> Task:
    """Task for creating an onboarding guide based on findings"""
    return Task(
        description=(
            "Based on the comprehensive analysis performed, create an onboarding guide for "
            "application owners who are new to Dynatrace. Your guide should:\n\n"
            "1. **Introduction to Dynatrace Observability**: Explain what Dynatrace monitors\n"
            "2. **Available Data Types**: Describe the types of data available:\n"
            "   - Problems and incidents\n"
            "   - Security vulnerabilities\n"
            "   - Logs, metrics, traces\n"
            "   - Entity relationships and dependencies\n"
            "3. **How to Use This Data**: Provide practical examples based on the current findings:\n"
            "   - How problems help identify issues proactively\n"
            "   - How security monitoring protects your application\n"
            "   - How logs provide detailed troubleshooting context\n"
            "   - How to correlate data across different sources\n"
            "4. **Best Practices**: Share recommendations for:\n"
            "   - Setting up alerts and notifications\n"
            "   - Regular monitoring routines\n"
            "   - Incident response workflows\n"
            "   - Security vulnerability management\n"
            "5. **Next Steps**: Guide them on how to get started with Dynatrace\n\n"
            "Make the guide practical, using real examples from the current analysis. "
            "Keep it concise but comprehensive."
        ),
        expected_output=(
            "A practical onboarding guide containing:\n"
            "- Overview of Dynatrace capabilities and data types\n"
            "- Real examples from the current analysis showing how each data type is useful\n"
            "- Step-by-step guidance on using Dynatrace for monitoring and troubleshooting\n"
            "- Best practices for observability and incident management\n"
            "- Actionable next steps for getting started\n"
            "- Tips for maximizing value from Dynatrace"
        ),
        agent=agent,
        context=context  # Receives context from synthesis task
    )
