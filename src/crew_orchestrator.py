"""
Crew Orchestrator - Main orchestration system for the multi-agent workflow
Coordinates specialist agents to analyze Dynatrace observability data
"""

from crewai import Crew, Process
from typing import Dict, Any
import json
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .agents.specialist_agents import (
    create_problem_analyst_agent,
    create_security_analyst_agent,
    create_log_analyst_agent,
    create_insights_synthesizer_agent,
    create_onboarding_guide_agent
)
from .agents.tasks import (
    create_problem_analysis_task,
    create_security_analysis_task,
    create_log_analysis_task,
    create_synthesis_task,
    create_onboarding_guide_task
)


class DynatraceObservabilityCrew:
    """
    Multi-agent system for comprehensive Dynatrace observability analysis
    """
    
    def __init__(self, verbose: bool = True):
        self.console = Console()
        self.verbose = verbose
        self.results = {}
        
    def create_crew(self) -> Crew:
        """Create and configure the crew with agents and tasks"""
        
        self.console.print(Panel.fit(
            "[bold cyan]Initializing Dynatrace Observability Multi-Agent System[/bold cyan]",
            border_style="cyan"
        ))
        
        # Create specialist agents
        self.console.print("\n[yellow]Creating specialist agents...[/yellow]")
        
        problem_analyst = create_problem_analyst_agent()
        self.console.print("  ✓ Problem Analyst Agent created")
        
        security_analyst = create_security_analyst_agent()
        self.console.print("  ✓ Security Analyst Agent created")
        
        log_analyst = create_log_analyst_agent()
        self.console.print("  ✓ Log Analyst Agent created")
        
        insights_synthesizer = create_insights_synthesizer_agent()
        self.console.print("  ✓ Insights Synthesizer Agent created")
        
        onboarding_guide = create_onboarding_guide_agent()
        self.console.print("  ✓ Onboarding Guide Agent created")
        
        # Create tasks
        self.console.print("\n[yellow]Defining agent tasks...[/yellow]")
        
        problem_task = create_problem_analysis_task(problem_analyst)
        self.console.print("  ✓ Problem Analysis Task defined")
        
        security_task = create_security_analysis_task(security_analyst)
        self.console.print("  ✓ Security Analysis Task defined")
        
        log_task = create_log_analysis_task(log_analyst, context=[problem_task, security_task])
        self.console.print("  ✓ Log Analysis Task defined")
        
        synthesis_task = create_synthesis_task(
            insights_synthesizer, 
            context=[problem_task, security_task, log_task]
        )
        self.console.print("  ✓ Synthesis Task defined")
        
        onboarding_task = create_onboarding_guide_task(
            onboarding_guide,
            context=[synthesis_task]
        )
        self.console.print("  ✓ Onboarding Guide Task defined")
        
        # Create crew with sequential process
        crew = Crew(
            agents=[
                problem_analyst,
                security_analyst,
                log_analyst,
                insights_synthesizer,
                onboarding_guide
            ],
            tasks=[
                problem_task,
                security_task,
                log_task,
                synthesis_task,
                onboarding_task
            ],
            process=Process.sequential,
            verbose=self.verbose,
            memory=False,  # Disable memory to reduce token usage
            cache=False     # Disable cache for fresh results
        )
        
        self.console.print("\n[bold green]✓ Crew initialized successfully![/bold green]\n")
        
        return crew
    
    def run_analysis(self) -> Dict[str, Any]:
        """Execute the multi-agent analysis workflow"""
        
        self.console.print(Panel.fit(
            "[bold magenta]Starting Dynatrace Observability Analysis[/bold magenta]\n"
            "[dim]This may take several minutes as agents analyze your environment...[/dim]",
            border_style="magenta"
        ))
        
        start_time = datetime.now()
        
        try:
            # Create and run the crew
            crew = self.create_crew()
            
            self.console.print("\n[bold yellow]Agents are working...[/bold yellow]\n")
            
            # Execute the crew
            result = crew.kickoff()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Store results
            self.results = {
                "status": "success",
                "timestamp": start_time.isoformat(),
                "duration_seconds": duration,
                "final_report": str(result),
                "metadata": {
                    "agents_count": len(crew.agents),
                    "tasks_count": len(crew.tasks)
                }
            }
            
            self.console.print(Panel.fit(
                f"[bold green]✓ Analysis Complete![/bold green]\n"
                f"[dim]Duration: {duration:.2f} seconds[/dim]",
                border_style="green"
            ))
            
            return self.results
            
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.results = {
                "status": "error",
                "timestamp": start_time.isoformat(),
                "duration_seconds": duration,
                "error": str(e)
            }
            
            self.console.print(Panel.fit(
                f"[bold red]✗ Analysis Failed[/bold red]\n"
                f"[dim]Error: {str(e)}[/dim]",
                border_style="red"
            ))
            
            raise
    
    def save_report(self, output_path: str = "reports/observability_report.md"):
        """Save the analysis report to a file"""
        
        if not self.results:
            self.console.print("[yellow]No results to save. Run analysis first.[/yellow]")
            return
        
        try:
            # Create markdown report
            report_content = self._format_markdown_report()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.console.print(f"\n[green]✓ Report saved to: {output_path}[/green]")
            
            # Also save JSON version
            json_path = output_path.replace('.md', '.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2)
            
            self.console.print(f"[green]✓ JSON data saved to: {json_path}[/green]")
            
        except Exception as e:
            self.console.print(f"[red]Error saving report: {str(e)}[/red]")
    
    def _format_markdown_report(self) -> str:
        """Format results as a markdown report"""
        
        report = f"""# Dynatrace Observability Analysis Report

**Generated:** {self.results.get('timestamp', 'N/A')}  
**Duration:** {self.results.get('duration_seconds', 0):.2f} seconds  
**Status:** {self.results.get('status', 'unknown').upper()}

---

## Analysis Results

{self.results.get('final_report', 'No report available')}

---

## Metadata

- **Agents Used:** {self.results.get('metadata', {}).get('agents_count', 'N/A')}
- **Tasks Executed:** {self.results.get('metadata', {}).get('tasks_count', 'N/A')}
- **Analysis Type:** Multi-Agent Sequential Workflow

---

*This report was generated by the Dynatrace Observability Multi-Agent System*
"""
        
        return report
    
    def display_summary(self):
        """Display a summary of the analysis results"""
        
        if not self.results:
            self.console.print("[yellow]No results to display. Run analysis first.[/yellow]")
            return
        
        self.console.print("\n" + "="*80)
        self.console.print(Panel.fit(
            "[bold cyan]ANALYSIS SUMMARY[/bold cyan]",
            border_style="cyan"
        ))
        
        self.console.print(f"\n[bold]Status:[/bold] {self.results.get('status', 'unknown')}")
        self.console.print(f"[bold]Duration:[/bold] {self.results.get('duration_seconds', 0):.2f} seconds")
        self.console.print(f"[bold]Timestamp:[/bold] {self.results.get('timestamp', 'N/A')}")
        
        if self.results.get('status') == 'success':
            self.console.print("\n[bold green]✓ Analysis completed successfully[/bold green]")
            self.console.print("\nFinal report has been generated. Use save_report() to export it.")
        else:
            self.console.print(f"\n[bold red]✗ Analysis failed: {self.results.get('error', 'Unknown error')}[/bold red]")
        
        self.console.print("="*80 + "\n")
