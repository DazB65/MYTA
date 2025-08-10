#!/usr/bin/env python3
"""
Comprehensive test runner for Vidalytics
Provides different test execution modes and reporting
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime


def run_command(command, description=""):
    """Run shell command and return success status"""
    print(f"\n{'='*60}")
    print(f"🚀 {description or command}")
    print(f"{'='*60}")
    
    try:
        # Convert string command to list for security (avoid shell=True)
        if isinstance(command, str):
            import shlex
            command_list = shlex.split(command)
        else:
            command_list = command
            
        result = subprocess.run(command_list, check=True, capture_output=False)
        print(f"✅ Success: {description or ' '.join(command_list) if isinstance(command_list, list) else command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description or command}")
        print(f"Exit code: {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def install_test_dependencies():
    """Install testing dependencies"""
    print("📦 Installing testing dependencies...")
    
    commands = [
        "pip install -r backend/requirements-test.txt",
        "pip install -e ."  # Install package in development mode
    ]
    
    for cmd in commands:
        if not run_command(cmd, f"Installing: {cmd}"):
            return False
    
    return True


def run_unit_tests(coverage=True, verbose=True):
    """Run unit tests"""
    cmd = "python -m pytest tests/unit/"
    
    if coverage:
        cmd += " --cov=backend --cov-report=html --cov-report=term-missing"
    
    if verbose:
        cmd += " -v"
    
    cmd += " --tb=short"
    
    return run_command(cmd, "Running unit tests")


def run_integration_tests(verbose=True):
    """Run integration tests"""
    cmd = "python -m pytest tests/integration/"
    
    if verbose:
        cmd += " -v"
    
    cmd += " --tb=short"
    
    return run_command(cmd, "Running integration tests")


def run_e2e_tests(verbose=True):
    """Run end-to-end tests"""
    cmd = "python -m pytest tests/e2e/"
    
    if verbose:
        cmd += " -v"
    
    cmd += " --tb=short --maxfail=3"  # Stop after 3 failures for e2e
    
    return run_command(cmd, "Running end-to-end tests")


def run_security_tests(verbose=True):
    """Run security tests"""
    cmd = "python -m pytest tests/security/"
    
    if verbose:
        cmd += " -v"
    
    cmd += " --tb=short"
    
    return run_command(cmd, "Running security tests")


def run_performance_tests():
    """Run performance/load tests"""
    cmd = "python -m pytest tests/ -m performance --tb=short"
    
    return run_command(cmd, "Running performance tests")


def run_all_tests(coverage=True):
    """Run all tests in order"""
    print("🎯 Running comprehensive test suite...")
    
    results = {
        "Unit Tests": run_unit_tests(coverage=coverage),
        "Integration Tests": run_integration_tests(),
        "Security Tests": run_security_tests(),
        "End-to-End Tests": run_e2e_tests(),
    }
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for test_type, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_type:<20} {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False


def run_quick_tests():
    """Run quick subset of tests for development"""
    cmd = "python -m pytest tests/unit/ tests/integration/ -x --tb=short --maxfail=5"
    return run_command(cmd, "Running quick test subset")


def run_security_scan():
    """Run security scanning tools"""
    print("🔒 Running security scans...")
    
    results = []
    
    # Bandit security scan
    results.append(run_command(
        "python -m bandit -r backend/ -f json -o security-report.json",
        "Running Bandit security scan"
    ))
    
    # Safety check for known vulnerabilities
    results.append(run_command(
        "python -m safety check --json --output safety-report.json",
        "Running Safety vulnerability check"
    ))
    
    return all(results)


def generate_coverage_report():
    """Generate detailed coverage report"""
    print("📈 Generating coverage report...")
    
    commands = [
        "python -m pytest tests/unit/ tests/integration/ --cov=backend --cov-report=html --cov-report=xml",
        "python -m coverage report --show-missing"
    ]
    
    for cmd in commands:
        run_command(cmd)


def run_lint_checks():
    """Run code quality checks"""
    print("🧹 Running code quality checks...")
    
    # Check if we have a linting setup
    lint_commands = []
    
    # Try different linting tools
    if Path("..").exists():
        lint_commands.extend([
            "python -m flake8 backend/ --max-line-length=88 --extend-ignore=E203,W503",
            "python -m black --check backend/",
            "python -m isort --check backend/"
        ])
    
    results = []
    for cmd in lint_commands:
        try:
            results.append(run_command(cmd, f"Linting: {cmd.split()[2]}"))
        except:
            print(f"⚠️  Linting tool not available: {cmd}")
            results.append(True)  # Don't fail if linting tools aren't installed
    
    return all(results)


def clean_test_artifacts():
    """Clean up test artifacts"""
    print("🧹 Cleaning up test artifacts...")
    
    cleanup_patterns = [
        ".pytest_cache",
        "htmlcov",
        "*.pyc",
        "__pycache__",
        ".coverage",
        "test-report.json",
        "test-report.html",
        "coverage.xml",
        "security-report.json",
        "safety-report.json"
    ]
    
    for pattern in cleanup_patterns:
        try:
            if "*" in pattern:
                run_command(f"find . -name '{pattern}' -delete", f"Cleaning {pattern}")
            else:
                run_command(f"rm -rf {pattern}", f"Cleaning {pattern}")
        except:
            pass  # Ignore cleanup errors


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description="Vidalytics Test Runner")
    parser.add_argument("--install", action="store_true", help="Install test dependencies")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests only")
    parser.add_argument("--security", action="store_true", help="Run security tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--quick", action="store_true", help="Run quick test subset")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--security-scan", action="store_true", help="Run security scans")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--clean", action="store_true", help="Clean test artifacts")
    parser.add_argument("--no-coverage", action="store_true", help="Skip coverage collection")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # If no specific test type is chosen, run all
    if not any([args.unit, args.integration, args.e2e, args.security, 
               args.performance, args.quick, args.coverage, args.security_scan, 
               args.lint, args.clean]):
        args.all = True
    
    print(f"🧪 Vidalytics Test Runner")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working directory: {Path.cwd()}")
    
    success = True
    
    try:
        if args.install:
            success &= install_test_dependencies()
        
        if args.clean:
            clean_test_artifacts()
        
        if args.lint:
            success &= run_lint_checks()
        
        if args.unit:
            success &= run_unit_tests(coverage=not args.no_coverage)
        
        if args.integration:
            success &= run_integration_tests()
        
        if args.e2e:
            success &= run_e2e_tests()
        
        if args.security:
            success &= run_security_tests()
        
        if args.performance:
            success &= run_performance_tests()
        
        if args.quick:
            success &= run_quick_tests()
        
        if args.coverage:
            generate_coverage_report()
        
        if args.security_scan:
            success &= run_security_scan()
        
        if args.all:
            success &= run_all_tests(coverage=not args.no_coverage)
    
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        success = False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        success = False
    
    finally:
        print(f"\n{'='*60}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if success:
            print("🎉 All tests completed successfully!")
            sys.exit(0)
        else:
            print("❌ Some tests failed or encountered errors")
            sys.exit(1)


if __name__ == "__main__":
    main()