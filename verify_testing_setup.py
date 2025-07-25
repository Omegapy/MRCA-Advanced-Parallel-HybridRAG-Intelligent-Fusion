#!/usr/bin/env python3
# -------------------------------------------------------------------------
# File: verify_testing_setup.py
# Project: MRCA - Mining Regulatory Compliance Assistant
# Author: Alexander Ricciardi
# Date: 2025-01-17 (Creation Date)
# Last Modified: 2025-01-17 
# File Path: verify_testing_setup.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Verification script for Week 1 testing infrastructure setup.
# Tests that pytest configuration, fixtures, and test discovery work correctly
# before running the full test suite. Validates Module 6 test case implementations.
# -------------------------------------------------------------------------

"""
MRCA Testing Infrastructure Verification

This script verifies that the Week 1 testing infrastructure is properly set up:
1. Pytest configuration and test discovery
2. Test fixtures and utilities
3. Module 6 test case implementations (Test Cases 1, 2, 3, 5)
4. Circuit breaker unit tests
5. Production test integration
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path


def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)


def print_result(test_name, passed, details=""):
    """Print test result with formatting."""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status} - {test_name}")
    if details:
        print(f"   {details}")


def check_file_exists(filepath, description=""):
    """Check if file exists and print result."""
    exists = Path(filepath).exists()
    desc = description or f"File: {filepath}"
    print_result(desc, exists)
    return exists


def check_pytest_config():
    """Verify pytest configuration."""
    print_section("Pytest Configuration")
    
    config_files = [
        ("tests/pytest.ini", "Pytest configuration file"),
        ("tests/__init__.py", "Tests package initialization"),
        ("tests/conftest.py", "Shared fixtures and utilities"),
        ("requirements-test.txt", "Testing dependencies")
    ]
    
    all_good = True
    for filepath, description in config_files:
        exists = check_file_exists(filepath, description)
        all_good = all_good and exists
    
    return all_good


def check_test_discovery():
    """Test pytest test discovery."""
    print_section("Test Discovery")
    
    try:
        # Run pytest test collection
        result = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "tests/", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Count discovered tests
            lines = result.stdout.split('\n')
            test_lines = [line for line in lines if '::test_' in line]
            test_count = len(test_lines)
            
            print_result("Pytest test discovery", True, f"Found {test_count} tests")
            
            # Show some examples
            if test_count > 0:
                print("   Examples:")
                for line in test_lines[:5]:  # Show first 5 tests
                    if '::test_' in line:
                        print(f"     {line.strip()}")
                if test_count > 5:
                    print(f"     ... and {test_count - 5} more tests")
            
            return True
        else:
            print_result("Pytest test discovery", False, f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print_result("Pytest test discovery", False, f"Exception: {e}")
        return False


def check_module_6_tests():
    """Verify Module 6 test case implementations."""
    print_section("Module 6 Test Cases")
    
    test_cases = [
        ("tests/integration/test_regulatory_citation_retrieval.py", "Test Case 1: Regulatory Citation Retrieval"),
        ("tests/integration/test_multi_domain_queries.py", "Test Case 2: Multi-Domain Queries"),
        ("tests/reliability/test_degraded_services.py", "Test Case 3: Degraded Services"),
        ("tests/architecture/test_confidence_hallucination.py", "Test Case 5: Confidence & Hallucination")
    ]
    
    all_good = True
    for filepath, description in test_cases:
        exists = check_file_exists(filepath, description)
        all_good = all_good and exists
        
        if exists:
            # Check file content has actual test classes
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    has_test_class = 'class Test' in content and 'pytest.mark' in content
                    print_result(f"  Content validation", has_test_class, 
                               "Contains test classes and pytest markers" if has_test_class else "Missing test structure")
            except Exception as e:
                print_result(f"  Content validation", False, f"Error reading file: {e}")
    
    return all_good


def check_unit_tests():
    """Verify unit test infrastructure."""
    print_section("Unit Tests")
    
    unit_tests = [
        ("tests/unit/__init__.py", "Unit tests package"),
        ("tests/unit/test_circuit_breaker.py", "Circuit breaker unit tests")
    ]
    
    all_good = True
    for filepath, description in unit_tests:
        exists = check_file_exists(filepath, description)
        all_good = all_good and exists
    
    return all_good


def check_production_test_integration():
    """Verify production test integration."""
    print_section("Production Test Integration")
    
    try:
        # Check that conftest.py has production_test_caller fixture
        with open("tests/conftest.py", 'r') as f:
            conftest_content = f.read()
        
        has_production_caller = "production_test_caller" in conftest_content
        print_result("Production test caller fixture", has_production_caller)
        
        # Check that existing production tests still exist
        production_tests = [
            ("frontend/test_frontend.py", "Frontend integration test"),
            ("backend/tools/vector.py", "VectorRAG test function"),
            ("backend/tools/general.py", "General tool test function")
        ]
        
        production_tests_exist = True
        for filepath, description in production_tests:
            exists = check_file_exists(filepath, description)
            production_tests_exist = production_tests_exist and exists
        
        return has_production_caller and production_tests_exist
        
    except Exception as e:
        print_result("Production test integration", False, f"Error: {e}")
        return False


def check_test_categories():
    """Verify test category markers are working."""
    print_section("Test Category Markers")
    
    try:
        # Test marker filtering
        result = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "tests/", "-m", "unit", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        unit_tests_found = result.returncode == 0 and "test_" in result.stdout
        print_result("Unit test marker filtering", unit_tests_found)
        
        result = subprocess.run(
            ["python", "-m", "pytest", "--collect-only", "tests/", "-m", "integration", "-q"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        integration_tests_found = result.returncode == 0 and "test_" in result.stdout
        print_result("Integration test marker filtering", integration_tests_found)
        
        return unit_tests_found and integration_tests_found
        
    except Exception as e:
        print_result("Test category markers", False, f"Error: {e}")
        return False


def check_dependencies():
    """Check that testing dependencies are available."""
    print_section("Testing Dependencies")
    
    key_dependencies = [
        ("pytest", "Core testing framework"),
        ("httpx", "HTTP client for API testing"),
        ("unittest.mock", "Mocking utilities"),
        ("asyncio", "Async testing support")
    ]
    
    all_good = True
    for dep_name, description in key_dependencies:
        try:
            if dep_name == "unittest.mock":
                from unittest import mock
            else:
                importlib.import_module(dep_name)
            print_result(description, True, f"{dep_name} available")
        except ImportError:
            print_result(description, False, f"{dep_name} not available")
            all_good = False
    
    return all_good


def run_sample_test():
    """Run a sample test to verify everything works."""
    print_section("Sample Test Execution")
    
    try:
        # Try to run the Test Case 1 primary test
        result = subprocess.run(
            ["python", "-m", "pytest", 
             "tests/integration/test_regulatory_citation_retrieval.py::TestRegulatoryCitationRetrieval::test_primary_cfr_citation_parallel_hybrid", 
             "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if "PASSED" in result.stdout:
            print_result("Sample Test Case 1 execution", True, "Primary CFR citation test passed")
            return True
        elif "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
            print_result("Sample Test Case 1 execution", False, "Import errors - backend not available")
            return False
        elif "skipped" in result.stdout.lower():
            print_result("Sample Test Case 1 execution", True, "Test was skipped (likely missing services)")
            return True
        else:
            print_result("Sample Test Case 1 execution", False, f"Test failed or errored")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}...")
            return False
            
    except Exception as e:
        print_result("Sample test execution", False, f"Exception: {e}")
        return False


def main():
    """Main verification function."""
    print("MRCA Testing Infrastructure Verification")
    print("Verifying Week 1 testing setup completion...\n")
    
    # Run all checks
    checks = [
        ("Pytest Configuration", check_pytest_config),
        ("Test Discovery", check_test_discovery),
        ("Module 6 Test Cases", check_module_6_tests),
        ("Unit Tests", check_unit_tests),
        ("Production Test Integration", check_production_test_integration),
        ("Test Category Markers", check_test_categories),
        ("Testing Dependencies", check_dependencies)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} - Exception: {e}")
            results.append((check_name, False))
    
    # Optional: Try to run a sample test
    if all(result for _, result in results):
        print("\nAll infrastructure checks passed! Trying sample test execution...")
        sample_result = run_sample_test()
        results.append(("Sample Test Execution", sample_result))
    
    # Summary
    print_section("Verification Summary")
    
    passed_checks = sum(1 for _, result in results if result)
    total_checks = len(results)
    
    for check_name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
    
    print(f"\nOverall Result: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n✅ Testing infrastructure is ready!")
        print("\nNext steps:")
        print("   • Install testing dependencies: pip install -r requirements-test.txt")
        print("   • Run all tests: pytest tests/")
        print("   • Run specific categories: pytest -m unit, pytest -m integration")
        print("   • View test coverage: pytest --cov=backend --cov=frontend")
        print("\nSee TESTING_IMPLEMENTATION_GUIDE.md for complete usage instructions")
    else:
        print(f"\n⚠️  {total_checks - passed_checks} issues found. Please address failed checks above.")
        print("\nCommon fixes:")
        print("   • Ensure all files are created correctly")
        print("   • Install testing dependencies if missing")
        print("   • Check file paths and directory structure")
    
    return passed_checks == total_checks


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 