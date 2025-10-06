"""
Comprehensive test for all MCP tools
Tests each tool with proper parameters
"""

import sys
from pathlib import Path
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

def test_tool(name, func, show_full=False):
    """Test a single tool and show results"""
    print(f"\n{'='*80}")
    print(f"Testing: {name}")
    print(f"{'='*80}")
    
    try:
        result = func()
        
        # Check if it's an error
        if result.startswith("Error"):
            print(f"❌ FAILED\n")
            print(result)
            return False
        else:
            print(f"✅ SUCCESS\n")
            if show_full:
                print(f"Full Result:\n{result}\n")
            else:
                # Show first 300 chars
                preview = result[:300] + "..." if len(result) > 300 else result
                print(f"Result Preview:\n{preview}\n")
            return True
            
    except Exception as e:
        print(f"❌ EXCEPTION\n")
        print(f"{type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("="*80)
    print("COMPREHENSIVE MCP TOOLS TEST")
    print("="*80)
    print("\nTesting all 7 integrated MCP tools...")
    
    results = {}
    
    # Test 1: Get Environment Info (we know this works)
    print("\n\n🧪 TEST 1/7: Get Environment Info")
    tool = GetEnvironmentInfoTool()
    results["GetEnvironmentInfo"] = test_tool(
        "Get Environment Info",
        lambda: tool._run()
    )
    
    # Test 2: List Problems (FAILING - let's see why)
    print("\n\n🧪 TEST 2/7: List Problems")
    tool = ListProblemsTool()
    results["ListProblems"] = test_tool(
        "List Problems",
        lambda: tool._run(),
        show_full=True  # Show full error
    )
    
    # Test 3: List Vulnerabilities
    print("\n\n🧪 TEST 3/7: List Vulnerabilities")
    tool = ListVulnerabilitiesTool()
    results["ListVulnerabilities"] = test_tool(
        "List Vulnerabilities",
        lambda: tool._run(risk_score=8.0),
        show_full=True  # Show full error
    )
    
    # Test 4: Execute DQL
    print("\n\n🧪 TEST 4/7: Execute DQL")
    tool = ExecuteDQLTool()
    results["ExecuteDQL"] = test_tool(
        "Execute DQL",
        lambda: tool._run(dql_statement="fetch logs | limit 5"),
        show_full=True  # Show full error
    )
    
    # Test 5: Generate DQL
    print("\n\n🧪 TEST 5/7: Generate DQL from Natural Language")
    tool = GenerateDQLTool()
    results["GenerateDQL"] = test_tool(
        "Generate DQL",
        lambda: tool._run(natural_language_query="Show me error logs from the last hour")
    )
    
    # Test 6: Find Entity
    print("\n\n🧪 TEST 6/7: Find Entity by Name")
    tool = FindEntityByNameTool()
    results["FindEntity"] = test_tool(
        "Find Entity",
        lambda: tool._run(entity_name="service")
    )
    
    # Test 7: Chat with Davis CoPilot
    print("\n\n🧪 TEST 7/7: Chat with Davis CoPilot")
    tool = ChatWithDavisCopilotTool()
    results["ChatDavisCopilot"] = test_tool(
        "Chat with Davis CoPilot",
        lambda: tool._run(message="What is Dynatrace?")
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
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\nFailed tests show detailed error messages above.")
    
    print("\n" + "="*80)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
