"""
Test script to verify MCP tool integration
Tests each tool individually before running the full agent system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.dynatrace_mcp_tools import (
    ListProblemsTool,
    ListVulnerabilitiesTool,
    ExecuteDQLTool,
    GenerateDQLTool,
    FindEntityByNameTool,
    ChatWithDavisCopilotTool,
    GetEnvironmentInfoTool
)

def test_tool(tool_name, tool, *args, **kwargs):
    """Test a single tool"""
    print(f"\n{'='*80}")
    print(f"Testing: {tool_name}")
    print(f"{'='*80}")
    
    try:
        result = tool._run(*args, **kwargs)
        print(f"✅ Success!")
        print(f"\nResult (first 500 chars):")
        print(result[:500] if len(result) > 500 else result)
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run all tool tests"""
    print("="*80)
    print("MCP Tool Integration Test")
    print("="*80)
    print("\nThis will test each MCP tool individually")
    print("Make sure your .env file is configured with:")
    print("  - DT_ENVIRONMENT")
    print("  - DT_PLATFORM_TOKEN")
    print("  - OPENAI_API_KEY")
    
    input("\nPress Enter to start tests...")
    
    results = {}
    
    # Test 1: Environment Info (simplest test)
    print("\n\n🧪 TEST 1: Get Environment Info")
    print("-" * 80)
    tool = GetEnvironmentInfoTool()
    results["GetEnvironmentInfo"] = test_tool("Get Environment Info", tool)
    
    # Test 2: List Problems
    print("\n\n🧪 TEST 2: List Problems")
    print("-" * 80)
    tool = ListProblemsTool()
    results["ListProblems"] = test_tool("List Problems", tool)
    
    # Test 3: List Vulnerabilities
    print("\n\n🧪 TEST 3: List Vulnerabilities")
    print("-" * 80)
    tool = ListVulnerabilitiesTool()
    results["ListVulnerabilities"] = test_tool("List Vulnerabilities", tool, risk_score=8.0)
    
    # Test 4: Generate DQL
    print("\n\n🧪 TEST 4: Generate DQL from Natural Language")
    print("-" * 80)
    tool = GenerateDQLTool()
    results["GenerateDQL"] = test_tool(
        "Generate DQL", 
        tool, 
        natural_language_query="Show me error logs from the last hour"
    )
    
    # Test 5: Execute DQL
    print("\n\n🧪 TEST 5: Execute DQL Query")
    print("-" * 80)
    tool = ExecuteDQLTool()
    results["ExecuteDQL"] = test_tool(
        "Execute DQL", 
        tool, 
        dql_statement="fetch logs | limit 5"
    )
    
    # Test 6: Find Entity
    print("\n\n🧪 TEST 6: Find Entity by Name")
    print("-" * 80)
    tool = FindEntityByNameTool()
    results["FindEntity"] = test_tool(
        "Find Entity", 
        tool, 
        entity_name="service"  # Generic search
    )
    
    # Test 7: Chat with Davis CoPilot
    print("\n\n🧪 TEST 7: Chat with Davis CoPilot")
    print("-" * 80)
    tool = ChatWithDavisCopilotTool()
    results["ChatDavisCopilot"] = test_tool(
        "Chat with Davis CoPilot", 
        tool, 
        message="What is Dynatrace?"
    )
    
    # Summary
    print("\n\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for tool_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {tool_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your MCP integration is working correctly.")
        print("\nYou can now run the full system with:")
        print("   python main.py")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\nCommon issues:")
        print("  1. MCP library not installed: pip install mcp")
        print("  2. Environment variables not set in .env")
        print("  3. Dynatrace token lacks required scopes")
        print("  4. Network connectivity issues")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
