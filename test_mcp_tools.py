"""
Test script to verify Dynatrace MCP tools work correctly
"""

from src.tools.dynatrace_mcp_tools import (
    ListProblemsTool,
    ListVulnerabilitiesTool,
    GetEnvironmentInfoTool
)

def test_tools():
    """Test each MCP tool"""
    
    print("=" * 80)
    print("Testing Dynatrace MCP Tools")
    print("=" * 80)
    
    # Test 1: Get Environment Info
    print("\n1. Testing GetEnvironmentInfoTool...")
    print("-" * 80)
    try:
        env_tool = GetEnvironmentInfoTool()
        result = env_tool._run()
        print("✅ Success!")
        print(f"Result: {result[:500]}...")  # First 500 chars
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 2: List Problems
    print("\n2. Testing ListProblemsTool...")
    print("-" * 80)
    try:
        problems_tool = ListProblemsTool()
        result = problems_tool._run(max_problems=5)
        print("✅ Success!")
        print(f"Result: {result[:500]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Test 3: List Vulnerabilities
    print("\n3. Testing ListVulnerabilitiesTool...")
    print("-" * 80)
    try:
        vuln_tool = ListVulnerabilitiesTool()
        result = vuln_tool._run(risk_score=8.0, max_vulnerabilities=5)
        print("✅ Success!")
        print(f"Result: {result[:500]}...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("✅ Tool testing complete!")
    print("=" * 80)
    print("\nIf all tests passed, your MCP tools are working correctly.")
    print("You can now run the full multi-agent system with: python main.py")


if __name__ == "__main__":
    test_tools()
