"""
Specialist Agents for Dynatrace Observability Analysis
Each agent is an expert in their domain: Problems, Security, Logs, and Analysis
"""

from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import List
from ..tools.dynatrace_mcp_tools import (
    ListProblemsTool,
    ListVulnerabilitiesTool,
    ExecuteDQLTool,
    GenerateDQLTool,
    FindEntityByNameTool,
    ChatWithDavisCopilotTool,
    GetEnvironmentInfoTool
)


def create_llm(temperature: float = 0.7):
    """Create an LLM instance for agents"""
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temperature
    )


def create_problem_analyst_agent() -> Agent:
    """
    Problem Analyst Agent - Expert in identifying and analyzing problems
    """
    return Agent(
        role="Problem Analyst",
        goal=(
            "Identify and analyze all open problems in Dynatrace, "
            "assess their severity and impact, and provide clear insights "
            "about what's affecting the system."
        ),
        backstory=(
            "You are an experienced Site Reliability Engineer with deep expertise "
            "in incident management and problem analysis. You have a keen eye for "
            "identifying critical issues and understanding their business impact. "
            "You excel at translating technical problems into actionable insights "
            "that application owners can understand and act upon."
        ),
        tools=[
            ListProblemsTool(),
            FindEntityByNameTool(),
            GetEnvironmentInfoTool()
        ],
        llm=create_llm(temperature=0.3),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )


def create_security_analyst_agent() -> Agent:
    """
    Security Analyst Agent - Expert in security vulnerabilities and risks
    """
    return Agent(
        role="Security Analyst",
        goal=(
            "Identify security vulnerabilities, assess their risk levels, "
            "and provide clear remediation guidance to protect the application "
            "and infrastructure from security threats."
        ),
        backstory=(
            "You are a cybersecurity expert with extensive experience in "
            "vulnerability management and threat analysis. You understand CVEs, "
            "security best practices, and how to prioritize security risks based "
            "on their potential impact. You communicate security issues in a way "
            "that non-security personnel can understand and act upon."
        ),
        tools=[
            ListVulnerabilitiesTool(),
            FindEntityByNameTool()
        ],
        llm=create_llm(temperature=0.3),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )


def create_log_analyst_agent() -> Agent:
    """
    Log Analyst Agent - Expert in log analysis and correlation
    """
    return Agent(
        role="Log Analyst",
        goal=(
            "Analyze logs to find error patterns, correlate log entries with "
            "problems and vulnerabilities, and extract meaningful insights "
            "from log data to support root cause analysis."
        ),
        backstory=(
            "You are a log analysis expert with years of experience in debugging "
            "complex distributed systems. You know how to filter through massive "
            "amounts of log data to find the needle in the haystack. You excel at "
            "pattern recognition and can quickly identify anomalies and error "
            "conditions that indicate underlying problems."
        ),
        tools=[
            ExecuteDQLTool(),
            GenerateDQLTool(),
            FindEntityByNameTool(),
            ChatWithDavisCopilotTool()
        ],
        llm=create_llm(temperature=0.4),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )


def create_insights_synthesizer_agent() -> Agent:
    """
    Insights Synthesizer Agent - Master agent that synthesizes all findings
    """
    return Agent(
        role="Observability Insights Synthesizer",
        goal=(
            "Synthesize findings from problem analysis, security assessment, and "
            "log analysis into a comprehensive, actionable report for application "
            "owners. Provide clear explanations of what data is available in "
            "Dynatrace and how it can be used to identify and resolve issues."
        ),
        backstory=(
            "You are a senior technical consultant specializing in observability "
            "and application performance management. You have a unique ability to "
            "take complex technical data from multiple sources and distill it into "
            "clear, actionable insights. You understand both the technical details "
            "and the business context, making you the perfect bridge between "
            "engineering teams and application owners. You excel at creating "
            "comprehensive reports that guide decision-making and problem resolution."
        ),
        tools=[],  # This agent synthesizes, doesn't need tools
        llm=create_llm(temperature=0.6),
        verbose=True,
        allow_delegation=False,
        max_iter=15
    )


def create_onboarding_guide_agent() -> Agent:
    """
    Onboarding Guide Agent - Helps new users understand Dynatrace capabilities
    """
    return Agent(
        role="Dynatrace Onboarding Guide",
        goal=(
            "Educate application owners about Dynatrace capabilities, explain "
            "what observability data is available, and guide them on how to use "
            "this data effectively for monitoring, troubleshooting, and optimization."
        ),
        backstory=(
            "You are a Dynatrace expert and educator with a passion for helping "
            "teams adopt observability best practices. You have deep knowledge of "
            "Dynatrace features, data types, and use cases. You excel at explaining "
            "complex concepts in simple terms and providing practical guidance that "
            "helps teams get immediate value from their observability platform."
        ),
        tools=[],
        llm=create_llm(temperature=0.7),
        verbose=True,
        allow_delegation=False,
        max_iter=10
    )
