#!/usr/bin/env python
"""
Test Runner Script
Run this script to execute all Selenium tests locally.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --smoke      # Run only smoke tests
    python run_tests.py --auth       # Run only auth tests
    python run_tests.py --todo       # Run only todo tests
"""

import subprocess
import sys
import os

def run_tests(marker=None):
    """Run pytest with optional marker filter."""
    
    # Base command
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",
        "--tb=short",
        "--html=reports/test_report.html",
        "--self-contained-html"
    ]
    
    # Add marker if specified
    if marker:
        cmd.extend(["-m", marker])
    
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    
    print(f"\n{'='*60}")
    print("🧪 Running Selenium Tests for MERN Todo Application")
    print(f"{'='*60}\n")
    
    # Run tests
    result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
    
    print(f"\n{'='*60}")
    if result.returncode == 0:
        print("✅ All tests passed!")
    else:
        print(f"❌ Some tests failed (exit code: {result.returncode})")
    print(f"{'='*60}\n")
    
    print("📄 Test report generated: reports/test_report.html")
    
    return result.returncode


if __name__ == "__main__":
    marker = None
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].replace("--", "")
        if arg in ["smoke", "auth", "todo"]:
            marker = arg
    
    exit_code = run_tests(marker)
    sys.exit(exit_code)
