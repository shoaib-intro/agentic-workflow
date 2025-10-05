"""
Main Entry Point for Dynatrace Observability Multi-Agent System

This system uses a hierarchical multi-agent architecture to analyze Dynatrace
observability data and provide comprehensive insights for application owners.

Architecture:
- Problem Analyst Agent: Identifies and analyzes open problems
- Security Analyst Agent: Identifies vulnerabilities and security risks
- Log Analyst Agent: Analyzes logs and correlates with problems
- Insights Synthesizer Agent: Synthesizes findings into actionable insights
- Onboarding Guide Agent: Creates educational content for new users

Usage:
    python main.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crew_orchestrator import DynatraceObservabilityCrew


def check_environment() -> bool:
    """Check if required environment variables are set"""
    console = Console()
    
    required_vars = {
        "DT_ENVIRONMENT": "Dynatrace environment URL",
        "DT_PLATFORM_TOKEN": "Dynatrace platform token",
        "OPENAI_API_KEY": "OpenAI API key for agents"
    }
    
    missing_vars = []
    
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  • {var}: {description}")
    
    if missing_vars:
        console.print(Panel.fit(
            "[bold red]Missing Required Environment Variables[/bold red]\n\n"
            "Please set the following variables in your .env file:\n\n" +
            "\n".join(missing_vars) +
            "\n\n[dim]Copy .env.example to .env and fill in your credentials.[/dim]",
            border_style="red"
        ))
        return False
    
    return True


def display_welcome():
    """Display welcome message and system information"""
    console = Console()
    
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Dynatrace Observability Multi-Agent System[/bold cyan]\n\n"
        "[dim]A hierarchical AI agent system for comprehensive observability analysis[/dim]\n\n"
        "This system will:\n"
        "  1. Analyze open problems and incidents\n"
        "  2. Identify security vulnerabilities\n"
        "  3. Correlate logs with issues\n"
        "  4. Synthesize actionable insights\n"
        "  5. Generate an onboarding guide\n\n"
        "[bold yellow]⚠ Note:[/bold yellow] This analysis may incur Dynatrace Grail query costs\n"
        "[dim]based on the volume of data scanned.[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))


def main():
    """Main execution function"""
    console = Console()
    
    # Load environment variables
    load_dotenv()
    
    # Display welcome message
    display_welcome()
    
    # Check environment configuration
    if not check_environment():
        console.print("\n[red]Exiting due to missing configuration.[/red]\n")
        sys.exit(1)
    
    # Display configuration
    console.print("\n[bold]Configuration:[/bold]")
    console.print(f"  • Dynatrace Environment: {os.getenv('DT_ENVIRONMENT')}")
    console.print(f"  • Token: {'*' * 20} (configured)")
    console.print(f"  • Grail Budget: {os.getenv('DT_GRAIL_QUERY_BUDGET_GB', '1000')} GB")
    
    # Confirm execution
    console.print("\n")
    if not Confirm.ask("[yellow]Start the analysis?[/yellow]", default=True):
        console.print("\n[dim]Analysis cancelled.[/dim]\n")
        sys.exit(0)
    
    try:
        # Create and run the crew
        crew_system = DynatraceObservabilityCrew(verbose=True)
        
        # Run analysis
        results = crew_system.run_analysis()
        
        # Display summary
        crew_system.display_summary()
        
        # Save report
        console.print("\n")
        if Confirm.ask("[yellow]Save the report?[/yellow]", default=True):
            timestamp = results.get('timestamp', '').replace(':', '-').split('.')[0]
            report_path = f"reports/observability_report_{timestamp}.md"
            crew_system.save_report(report_path)
        
        # Display final report
        console.print("\n" + "="*80)
        console.print(Panel.fit(
            "[bold green]FINAL REPORT[/bold green]",
            border_style="green"
        ))
        console.print("\n" + results.get('final_report', 'No report available'))
        console.print("\n" + "="*80 + "\n")
        
        console.print("[bold green]✓ Analysis completed successfully![/bold green]\n")
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Analysis interrupted by user.[/yellow]\n")
        sys.exit(0)
        
    except Exception as e:
        console.print(f"\n[bold red]Error during analysis:[/bold red] {str(e)}\n")
        
        # Print detailed error for debugging
        import traceback
        console.print("[dim]Detailed error:[/dim]")
        console.print(traceback.format_exc())
        
        sys.exit(1)


if __name__ == "__main__":
    main()
