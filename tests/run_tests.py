"""
Test runner script for Vidalytics testing infrastructure
Provides organized test execution with coverage reporting and filtering
"""
import subprocess
import sys
import argparse
import os
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return the result"""
    if description:
        print(f"\n🔄 {description}")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description or 'Command'} completed successfully")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ {description or 'Command'} failed")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Run Vidalytics tests")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "e2e", "security", "performance", "all"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip slow tests"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Run specific test file"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    
    args = parser.parse_args()
    
    # Set up base pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test directory
    test_dir = Path(__file__).parent
    
    if args.file:
        # Run specific file
        cmd.append(str(test_dir / args.file))
    else:
        # Add test type filter
        if args.type == "unit":
            cmd.extend(["-m", "unit", str(test_dir / "unit")])
        elif args.type == "integration":
            cmd.extend(["-m", "integration", str(test_dir / "integration")])
        elif args.type == "e2e":
            cmd.extend(["-m", "e2e", str(test_dir / "e2e")])
        elif args.type == "security":
            cmd.extend(["-m", "security", str(test_dir / "security")])
        elif args.type == "performance":
            cmd.extend(["-m", "performance"])
        else:
            cmd.append(str(test_dir))
    
    # Add coverage
    if args.coverage:
        cmd.extend([
            "--cov=backend",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-report=xml"
        ])
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")
    
    # Skip slow tests
    if args.fast:
        cmd.extend(["-m", "not slow"])
    
    # Parallel execution
    if args.parallel:
        try:
            import pytest_xdist
            cmd.extend(["-n", "auto"])
        except ImportError:
            print("⚠️  pytest-xdist not installed. Running tests sequentially.")
    
    # Additional pytest options
    cmd.extend([
        "--tb=short",
        "--strict-markers",
        "--disable-warnings",
        "-x"  # Stop on first failure
    ])
    
    # Set environment variables
    env = os.environ.copy()
    env["ENVIRONMENT"] = "testing"
    env["PYTHONPATH"] = str(Path(__file__).parent.parent)
    
    print(f"🧪 Running {args.type} tests...")
    print(f"📁 Test directory: {test_dir}")
    
    # Run the tests
    result = subprocess.run(cmd, env=env)
    
    if result.returncode == 0:
        print("\n🎉 All tests passed!")
        
        if args.coverage:
            print("\n📊 Coverage report generated:")
            print("  - HTML: htmlcov/index.html")
            print("  - XML: coverage.xml")
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)


def run_quick_check():
    """Run a quick smoke test to verify basic functionality"""
    print("🚀 Running quick smoke test...")
    
    cmd = [
        "python", "-m", "pytest",
        str(Path(__file__).parent / "unit" / "test_youtube_analytics_service.py::TestYouTubeAnalyticsService::test_initialization"),
        "-v"
    ]
    
    result = run_command(cmd, "Quick smoke test")
    return result.returncode == 0


def run_full_test_suite():
    """Run the complete test suite with coverage"""
    print("🏃‍♂️ Running full test suite with coverage...")
    
    test_dir = Path(__file__).parent
    
    # Run tests in order: unit -> integration -> e2e
    test_types = [
        ("unit", "Unit tests"),
        ("integration", "Integration tests"),
        # ("e2e", "End-to-end tests")  # Uncomment when e2e tests are ready
    ]
    
    all_passed = True
    
    for test_type, description in test_types:
        cmd = [
            "python", "-m", "pytest",
            "-m", test_type,
            str(test_dir / test_type),
            "-v",
            "--tb=short"
        ]
        
        result = run_command(cmd, f"{description} ({test_type})")
        if result.returncode != 0:
            all_passed = False
    
    # Run coverage report
    if all_passed:
        print("\n📊 Generating coverage report...")
        cmd = [
            "python", "-m", "pytest",
            str(test_dir),
            "--cov=backend",
            "--cov-report=html",
            "--cov-report=term-missing",
            "-v"
        ]
        run_command(cmd, "Coverage analysis")
    
    return all_passed


def check_test_dependencies():
    """Check if all test dependencies are installed"""
    required_packages = [
        "pytest",
        "pytest-asyncio", 
        "pytest-cov",
        "httpx",
        "fastapi",
    ]
    
    optional_packages = [
        ("pytest-xdist", "Parallel test execution"),
        ("pytest-html", "HTML test reports"),
        ("pytest-benchmark", "Performance benchmarking")
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_required.append(package)
    
    for package, description in optional_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_optional.append((package, description))
    
    if missing_required:
        print("❌ Missing required packages:")
        for package in missing_required:
            print(f"  - {package}")
        print("\nInstall with: pip install " + " ".join(missing_required))
        return False
    
    if missing_optional:
        print("⚠️  Missing optional packages:")
        for package, description in missing_optional:
            print(f"  - {package}: {description}")
        print("\nConsider installing for enhanced testing features")
    
    print("✅ All required test dependencies are installed")
    return True


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - show menu
        print("🧪 Vidalytics Test Runner")
        print("=" * 40)
        print("1. Quick smoke test")
        print("2. Run full test suite") 
        print("3. Check dependencies")
        print("4. Unit tests only")
        print("5. Integration tests only")
        print("6. Custom (use --help for options)")
        print()
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            success = run_quick_check()
            sys.exit(0 if success else 1)
        elif choice == "2":
            success = run_full_test_suite()
            sys.exit(0 if success else 1)
        elif choice == "3":
            success = check_test_dependencies()
            sys.exit(0 if success else 1)
        elif choice == "4":
            sys.argv = ["run_tests.py", "--type", "unit", "--verbose"]
        elif choice == "5":
            sys.argv = ["run_tests.py", "--type", "integration", "--verbose"]
        elif choice == "6":
            print("Use python run_tests.py --help for all options")
            sys.exit(0)
        else:
            print("Invalid choice")
            sys.exit(1)
    
    # Run with arguments
    main()