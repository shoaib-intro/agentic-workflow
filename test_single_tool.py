"""
Quick test to verify a single MCP tool works
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.dynatrace_mcp_tools import GetEnvironmentInfoTool

def test_single_tool():
    print("="*80)
    print("Testing Single MCP Tool")
    print("="*80)
    
    print("\nTesting: Get Environment Info")
    print("-"*80)
    
    tool = GetEnvironmentInfoTool()
    
    try:
        result = tool._run()
        print(f"\n✅ Tool executed successfully!\n")
        print(f"Result:\n{result}\n")
        
        if result and not result.startswith("Error"):
            print("✅ Tool is working correctly!")
            return True
        else:
            print("❌ Tool returned an error")
            return False
            
    except Exception as e:
        print(f"\n❌ Tool failed with exception:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_single_tool()
    sys.exit(0 if success else 1)
