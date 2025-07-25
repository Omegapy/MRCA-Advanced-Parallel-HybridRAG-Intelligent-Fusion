# -------------------------------------------------------------------------
# File: conftest.py
# Project: MRCA - Mining Regulatory Compliance Assistant
#          Advanced Parallel HybridRAG - Intelligent Fusion System
# Author: Alexander Ricciardi
# Last Modified: 2025-07-25
# File Path: tests/conftest.py
# ------------------------------------------------------------------------

# --- Module Objective ---
# Pytest configuration and shared fixtures for the MRCA testing framework.
# Provides reusable test fixtures, mock objects, and testing utilities
# that can be used across all test modules. Integrates with existing
# production tests where appropriate.

# --- Apache-2.0 ---
# © 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
# License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System
# -------------------------------------------------------------------------

"""
MRCA Testing Fixtures and Configuration

Shared pytest fixtures and utilities for comprehensive MRCA testing.
Provides integration with existing production test functions while
adding formal testing infrastructure.
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, Optional
import time
import requests
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import testing constants
from tests import (
    TEST_TIMEOUT_SHORT, TEST_TIMEOUT_MEDIUM, TEST_TIMEOUT_LONG,
    SAMPLE_CFR_QUERIES, SAMPLE_OFF_DOMAIN_QUERIES,
    ASR_THRESHOLDS, HEALTH_CHECK_ENDPOINTS, CIRCUIT_BREAKER_SERVICES
)

# =========================================================================
# Session-Level Fixtures
# =========================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def backend_url():
    """Backend API base URL for testing."""
    return "http://localhost:8000"

@pytest.fixture(scope="session")
def frontend_url():
    """Frontend UI base URL for testing."""
    return "http://localhost:8501"

# =========================================================================
# Mock Service Fixtures
# =========================================================================

@pytest.fixture
def mock_neo4j_healthy():
    """Mock healthy Neo4j connection."""
    with patch('backend.graph.graph') as mock_graph:
        mock_graph.query.return_value = [{"test": 1}]
        mock_graph.get_schema = Mock(return_value="Mock schema")
        yield mock_graph

@pytest.fixture
def mock_neo4j_failing():
    """Mock failing Neo4j connection."""
    with patch('backend.graph.graph') as mock_graph:
        mock_graph.query.side_effect = Exception("Connection failed")
        yield mock_graph

@pytest.fixture
def mock_openai_healthy():
    """Mock healthy OpenAI LLM connection."""
    mock_response = Mock()
    mock_response.content = "Test response from OpenAI"
    
    with patch('backend.llm.get_llm') as mock_llm:
        mock_llm.return_value.invoke.return_value = mock_response
        yield mock_llm

@pytest.fixture
def mock_openai_failing():
    """Mock failing OpenAI LLM connection."""
    with patch('backend.llm.get_llm') as mock_llm:
        mock_llm.return_value.invoke.side_effect = Exception("API key invalid")
        yield mock_llm

@pytest.fixture
def mock_gemini_healthy():
    """Mock healthy Gemini embeddings."""
    with patch('backend.llm.get_embeddings') as mock_embeddings:
        mock_embeddings.return_value.embed_query.return_value = [0.1] * 768
        yield mock_embeddings

@pytest.fixture
def mock_gemini_failing():
    """Mock failing Gemini embeddings."""
    with patch('backend.llm.get_embeddings') as mock_embeddings:
        mock_embeddings.return_value.embed_query.side_effect = Exception("Embedding failed")
        yield mock_embeddings

# =========================================================================
# Circuit Breaker Fixtures
# =========================================================================

@pytest.fixture
def reset_circuit_breakers():
    """Reset all circuit breakers before test."""
    try:
        from backend.circuit_breaker import reset_all_circuit_breakers
        reset_all_circuit_breakers()
    except ImportError:
        pass  # Circuit breaker module may not be available
    yield
    # Reset again after test
    try:
        reset_all_circuit_breakers()
    except ImportError:
        pass

@pytest.fixture
def mock_circuit_breaker_config():
    """Mock circuit breaker configuration for testing."""
    return {
        "failure_threshold": 2,  # Lower threshold for faster testing
        "timeout_duration": 1.0,  # Short timeout for testing
        "success_threshold": 1,   # Quick recovery for testing
        "max_timeout_duration": 5.0,
        "backoff_multiplier": 1.5
    }

# =========================================================================
# Test Data Fixtures
# =========================================================================

@pytest.fixture
def sample_cfr_queries():
    """Sample CFR regulation queries for testing."""
    return SAMPLE_CFR_QUERIES.copy()

@pytest.fixture
def sample_off_domain_queries():
    """Sample off-domain queries for testing."""
    return SAMPLE_OFF_DOMAIN_QUERIES.copy()

@pytest.fixture
def sample_regulatory_response():
    """Sample regulatory response for testing."""
    return {
        "response": "According to 30 CFR 56.12016, electrical equipment must be properly grounded...",
        "confidence": 0.92,
        "sources": ["30 CFR 56.12016"],
        "processing_time": 2.5
    }

@pytest.fixture
def sample_parallel_hybrid_response():
    """Sample Advanced Parallel Hybrid response."""
    return {
        "response": "Mining ventilation requirements are outlined in multiple CFR sections...",
        "vector_confidence": 0.89,
        "graph_confidence": 0.76,
        "final_confidence": 0.95,
        "fusion_strategy": "advanced_hybrid",
        "fusion_ready": True,
        "processing_metadata": {
            "total_time": 4.2,
            "vector_time": 1.1,
            "graph_time": 1.3,
            "fusion_time": 0.8,
            "template_time": 1.0
        }
    }

# =========================================================================
# Performance Testing Fixtures
# =========================================================================

@pytest.fixture
def performance_timer():
    """Timer utility for performance testing."""
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
            return self.elapsed
        
        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
    
    return Timer()

@pytest.fixture
def asr_thresholds():
    """ASR validation thresholds from Module 6 testing plan."""
    return ASR_THRESHOLDS.copy()

# =========================================================================
# Health Check Fixtures
# =========================================================================

@pytest.fixture
def health_checker():
    """Utility for checking service health."""
    class HealthChecker:
        def __init__(self):
            self.timeout = TEST_TIMEOUT_SHORT
        
        def check_endpoint(self, url: str) -> Dict[str, Any]:
            """Check health of a specific endpoint."""
            try:
                response = requests.get(url, timeout=self.timeout)
                return {
                    "healthy": response.status_code == 200,
                    "status_code": response.status_code,
                    "response_data": response.json() if response.status_code == 200 else None,
                    "error": None
                }
            except Exception as e:
                return {
                    "healthy": False,
                    "status_code": None,
                    "response_data": None,
                    "error": str(e)
                }
        
        def check_all_services(self) -> Dict[str, Dict[str, Any]]:
            """Check health of all MRCA services."""
            results = {}
            for service_name, url in HEALTH_CHECK_ENDPOINTS.items():
                results[service_name] = self.check_endpoint(url)
            return results
    
    return HealthChecker()

# =========================================================================
# Integration Test Fixtures
# =========================================================================

@pytest.fixture
def production_test_caller():
    """Utility to call existing production test functions."""
    class ProductionTestCaller:
        """Calls existing test functions from production modules."""
        
        def call_vector_test(self):
            """Call the existing vector test function."""
            try:
                from backend.tools.vector import test_vector_search
                test_vector_search()
                return True
            except Exception as e:
                return False, str(e)
        
        def call_general_test(self):
            """Call the existing general tool test function."""
            try:
                from backend.tools.general import test_general_tool
                test_general_tool()
                return True
            except Exception as e:
                return False, str(e)
        
        async def call_fusion_test(self):
            """Call the existing context fusion test function."""
            try:
                from backend.context_fusion import test_context_fusion
                await test_context_fusion()
                return True
            except Exception as e:
                return False, str(e)
        
        async def call_parallel_test(self):
            """Call the existing parallel retrieval test function."""
            try:
                from backend.parallel_hybrid import test_parallel_retrieval
                await test_parallel_retrieval()
                return True
            except Exception as e:
                return False, str(e)
        
        def call_frontend_test(self):
            """Call the existing frontend test function."""
            try:
                import sys
                frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
                sys.path.insert(0, frontend_path)
                
                from test_frontend import main
                return main()
            except Exception as e:
                return False, str(e)
    
    return ProductionTestCaller()

# =========================================================================
# Pytest Hooks and Configuration
# =========================================================================

def pytest_configure(config):
    """Configure pytest settings."""
    # Add custom markers
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "reliability" in str(item.fspath):
            item.add_marker(pytest.mark.reliability)
        elif "architecture" in str(item.fspath):
            item.add_marker(pytest.mark.architecture)

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically set up test environment for each test."""
    # Ensure clean state before each test
    os.environ.setdefault('TESTING', 'true')
    yield
    # Cleanup after test if needed 