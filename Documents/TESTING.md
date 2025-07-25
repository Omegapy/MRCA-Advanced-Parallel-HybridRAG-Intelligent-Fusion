# MRCA Advanced Parallel Hybrid Testing Infrastructure

---

## Mining Regulatory Compliance Assistant - Advanced Parallel Hybrid - Intelligent Fusion System

---

**Author:** Alexander Ricciardi  
**Project:** MRCA - Mining Regulatory Compliance Assistant  
**Version:** beta 2.0.0   
**Last Updated:** July 2025  

© 2025 Alexander Samuel Ricciardi - Mining Regulatory Compliance Assistant  
License: Apache-2.0 | Technology: Advanced Parallel HybridRAG - Intelligent Fusion System

---

This document was created by a human with the help of generative AI.

---

## 📋 **Overview**

This document provides comprehensive guidance for the MRCA Advanced Parallel Hybrid testing infrastructure, including local testing workflows, CI/CD pipeline configuration, and test coverage reporting.

## 🏗️ **Testing Architecture**

The MRCA testing suite is organized into multiple categories for comprehensive coverage:

### Test Categories

| Category | Purpose | Location | Speed | Dependencies |
|----------|---------|----------|-------|--------------|
| **Unit** | Individual component testing | `tests/unit/` | Fast | None |
| **Integration** | Module 6 test cases (1-5) | `tests/integration/` | Medium | API |  
| **Reliability** | Fault injection & load testing | `tests/reliability/` | Slow | API + Load |
| **Architecture** | Confidence & hallucination prevention | `tests/architecture/` | Medium | API |
| **E2E** | Complete user workflows | `tests/e2e/` | Slow | Full App |

### Test Infrastructure Files

```
tests/
├── __init__.py              # Test package configuration
├── conftest.py              # Shared fixtures and utilities
├── pytest.ini              # Pytest configuration
├── unit/                    # Unit tests
│   ├── __init__.py
│   └── test_circuit_breaker.py
├── integration/             # Integration tests  
│   ├── __init__.py
│   ├── test_regulatory_citation_retrieval.py (Test Case 1)
│   └── test_multi_domain_queries.py (Test Case 2)
├── reliability/             # Reliability tests
│   ├── __init__.py
│   ├── test_degraded_services.py (Test Case 3)
│   └── test_load_testing_fault_injection.py (Test Case 4)
├── architecture/            # Architecture tests
│   ├── __init__.py
│   └── test_confidence_hallucination.py (Test Case 5)
└── e2e/                     # End-to-end tests
    ├── __init__.py
    └── test_complete_user_workflows.py
```

## 🚀 **Local Testing**

### Quick Start

```bash
# Install testing dependencies
pip install -r requirements-test.txt

# Run fast test suite (recommended for development)
python scripts/run_tests.py fast

# Run specific test categories
python scripts/run_tests.py unit
python scripts/run_tests.py integration
python scripts/run_tests.py reliability

# Run all tests
python scripts/run_tests.py all
```

### Test Runner Script

The `scripts/run_tests.py` script provides a unified interface for test execution:

```bash
# Basic usage
python scripts/run_tests.py [category] [options]

# Examples
python scripts/run_tests.py unit --no-coverage
python scripts/run_tests.py fast --parallel 
python scripts/run_tests.py all --max-failures 5
python scripts/run_tests.py unit integration --fail-fast
```

#### Available Options

- `--no-coverage`: Disable coverage reporting
- `--no-junit`: Disable JUnit XML output  
- `--quiet`: Reduce verbosity
- `--fail-fast`: Stop on first failure
- `--max-failures N`: Stop after N failures
- `--parallel`: Run tests in parallel (where supported)
- `--output-dir DIR`: Set output directory for results
- `--markers`: Additional pytest markers

### Direct Pytest Usage

```bash
# Run unit tests with coverage
pytest tests/unit/ -v --cov=backend --cov-report=xml

# Run integration tests (Module 6 test cases)
pytest tests/integration/ -v

# Run with specific markers
pytest -m "unit and not slow" -v

# Run E2E tests (requires running application)
pytest tests/e2e/ -v --tb=short
```

## 🔄 **CI/CD Pipeline**

### GitHub Actions Workflow

The CI/CD pipeline in `.github/workflows/test-suite.yml` provides three execution levels:

#### 1. Fast Tests (Pull Requests)
- **Trigger**: All pull requests
- **Includes**: Unit tests + basic integration tests
- **Duration**: ~3-5 minutes
- **Coverage**: Yes

#### 2. Comprehensive Tests (Pushes to main/develop)
- **Trigger**: Pushes to main/develop branches  
- **Includes**: All tests except E2E and load tests
- **Duration**: ~10-15 minutes
- **Services**: Neo4j database
- **Coverage**: Yes

#### 3. Full Tests (Scheduled + Manual)
- **Trigger**: Daily at 2 AM UTC + manual dispatch
- **Includes**: Complete test suite with E2E and load tests
- **Duration**: ~20-30 minutes
- **Services**: Neo4j + full MRCA application
- **Coverage**: Yes

### Manual Workflow Dispatch

You can manually trigger workflows with different test levels:

1. Go to GitHub Actions tab
2. Select "MRCA Comprehensive Test Suite"
3. Click "Run workflow"
4. Choose test level: `fast`, `comprehensive`, or `full`

### Required Secrets

For full testing functionality, configure these GitHub secrets:

```
GEMINI_API_KEY_TEST: Test API key for Gemini integration
```

## 📊 **Coverage Reporting**

### Configuration

Coverage is configured via `.coveragerc`:

- **Source**: `backend/` directory
- **Branch Coverage**: Enabled
- **HTML Reports**: `htmlcov/` directory
- **XML Reports**: `coverage.xml` (for CI/CD)
- **Exclusions**: Test files, cache files, virtual environments

### Local Coverage Reports

```bash
# Generate coverage with HTML report
python scripts/run_tests.py unit --coverage
open htmlcov/index.html

# Generate only XML (for CI/CD integration)
pytest tests/unit/ --cov=backend --cov-report=xml
```

### Coverage Integration

- **Codecov**: Automatic upload in CI/CD pipeline
- **GitHub**: Coverage reports available as artifacts
- **Local**: HTML reports for detailed analysis

## 🧪 **Test Categories Deep Dive**

### Unit Tests (`tests/unit/`)

**Purpose**: Test individual components in isolation

**Key Tests**:
- `test_circuit_breaker.py`: Comprehensive circuit breaker testing (38 tests)
  - Configuration validation
  - State transitions  
  - Exponential backoff
  - Metrics tracking
  - Async support
  - Registry management

**Markers**: `@pytest.mark.unit`

**Speed**: Fast (~30 seconds)

### Integration Tests (`tests/integration/`)

**Purpose**: Test Module 6 Test Cases with real system integration

**Key Tests**:
- **Test Case 1**: `test_regulatory_citation_retrieval.py`
  - Direct CFR citation queries
  - Multiple citation handling
  - Performance benchmarks
- **Test Case 2**: `test_multi_domain_queries.py`  
  - Cross-domain query processing
  - Domain boundary validation
  - Query complexity scaling

**Markers**: `@pytest.mark.integration`, `@pytest.mark.requires_api`

**Speed**: Medium (~2-5 minutes)

### Reliability Tests (`tests/reliability/`)

**Purpose**: Test system resilience and fault tolerance

**Key Tests**:
- **Test Case 3**: `test_degraded_services.py`
  - Service degradation scenarios
  - Circuit breaker activation
  - Graceful degradation validation
- **Test Case 4**: `test_load_testing_fault_injection.py`
  - Concurrent user simulation
  - Fault injection during load
  - Performance under stress

**Markers**: `@pytest.mark.reliability`, `@pytest.mark.slow`

**Speed**: Slow (~5-10 minutes)

### Architecture Tests (`tests/architecture/`)

**Purpose**: Test system architecture and quality attributes

**Key Tests**:
- **Test Case 5**: `test_confidence_hallucination.py`
  - Off-domain query detection
  - Confidence threshold validation
  - Hallucination prevention
  - Domain boundary enforcement

**Markers**: `@pytest.mark.architecture`

**Speed**: Medium (~2-3 minutes)

### End-to-End Tests (`tests/e2e/`)

**Purpose**: Test complete user workflows and cross-component integration

**Key Tests**:
- `test_complete_user_workflows.py`
  - Health check workflows
  - Advanced Parallel Hybrid query workflows
  - Error handling and recovery
  - Fusion strategy comparison
  - Session management
  - Cross-component integration

**Markers**: `@pytest.mark.e2e`, `@pytest.mark.requires_api`

**Speed**: Slow (~10-15 minutes)

## 🔍 **Test Execution Examples**

### Development Workflow

```bash
# 1. Quick validation during development
python scripts/run_tests.py unit

# 2. Pre-commit validation
python scripts/run_tests.py fast

# 3. Feature testing with integration
python scripts/run_tests.py unit integration

# 4. Full validation before release
python scripts/run_tests.py all
```

### CI/CD Testing

```bash
# Fast tests (equivalent to PR checks)
python scripts/run_tests.py fast --no-coverage --junit-xml

# Comprehensive tests (equivalent to push to main)
python scripts/run_tests.py unit integration architecture reliability

# Full tests (equivalent to scheduled runs)  
python scripts/run_tests.py all --parallel
```

### Performance Testing

```bash
# Reliability tests only
python scripts/run_tests.py reliability

# Load testing specifically
pytest tests/reliability/test_load_testing_fault_injection.py -v

# E2E workflows
pytest tests/e2e/ -v --tb=short
```

## 📈 **Metrics and Reporting**

### Test Metrics Tracked

- **Execution Time**: Per test category and overall
- **Pass/Fail Counts**: Detailed breakdown by category
- **Coverage Percentage**: Line and branch coverage
- **Failure Analysis**: Error categorization and patterns

### Available Reports

1. **JUnit XML**: Machine-readable test results
2. **Coverage XML**: For CI/CD integration  
3. **Coverage HTML**: Detailed local analysis
4. **Test Summary**: Human-readable execution summary

### Performance Benchmarks

| Test Category | Expected Duration | Acceptable Range |
|---------------|-------------------|------------------|
| Unit | 30s | 15-60s |
| Integration | 3m | 2-5m |  
| Reliability | 8m | 5-15m |
| Architecture | 2m | 1-5m |
| E2E | 12m | 8-20m |
| **Total (All)** | **25m** | **15-45m** |

## 🛠️ **Troubleshooting**

### Common Issues

#### 1. Application Not Running (E2E Tests)
```bash
# Start the application first
python3 launch_devcontainer.py

# Verify services are running
curl http://localhost:8000/health
curl http://localhost:8501/_stcore/health
```

#### 2. Neo4j Connection Issues
```bash
# Check Neo4j status in Docker
docker ps | grep neo4j

# Restart if needed
docker-compose restart neo4j
```

#### 3. Coverage Issues
```bash
# Clear previous coverage data
rm .coverage coverage.xml

# Run with fresh coverage
python scripts/run_tests.py unit --coverage
```

#### 4. Test Dependencies Missing
```bash
# Reinstall test requirements
pip install -r requirements-test.txt

# Verify pytest is available
python -m pytest --version
```

### Environment Setup

```bash
# Complete test environment setup
pip install -r requirements.txt
pip install -r requirements-test.txt

# Create test configuration
mkdir -p .streamlit
cp .streamlit/secrets.toml.template .streamlit/secrets.toml

# Verify test discovery
pytest --collect-only -q
```

## 🎯 **Best Practices**

### Test Development

1. **Write Tests First**: Follow TDD when adding new features
2. **Use Appropriate Categories**: Choose the right test type for your scenario
3. **Mock External Dependencies**: Use fixtures for consistent test environments
4. **Test Edge Cases**: Include boundary conditions and error scenarios
5. **Keep Tests Independent**: Each test should be able to run in isolation

### Continuous Integration

1. **Run Fast Tests Locally**: Before committing code
2. **Monitor Coverage**: Maintain >80% coverage for critical components
3. **Fix Failing Tests Immediately**: Don't let technical debt accumulate
4. **Review Test Results**: Analyze failures and performance trends
5. **Update Tests with Code**: Keep tests synchronized with implementation changes

### Performance Optimization

1. **Use Parallel Execution**: For independent test categories
2. **Mock Heavy Operations**: Replace slow external calls with mocks
3. **Optimize Test Data**: Use minimal datasets for validation
4. **Cache Dependencies**: Reuse expensive setup operations
5. **Profile Slow Tests**: Identify and optimize bottlenecks

## 🔗 **Integration Points**

### With MRCA Application

- **Health Endpoints**: `/health`, `/parallel_hybrid/health`
- **API Endpoints**: `/generate_parallel_hybrid`, `/metrics`
- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000

### With External Services  

- **Neo4j**: Graph database for knowledge graph testing
- **Gemini API**: LLM integration for response generation
- **Circuit Breakers**: Fault tolerance testing

### With Development Tools

- **VS Code**: Test discovery and execution
- **GitHub Actions**: Automated CI/CD pipeline
- **Codecov**: Coverage reporting and analysis
- **Docker**: Containerized testing environments

## 📚 **Additional Resources**

- **Module 6 Test Cases**: See `Documents/MRCA Development Documentation.md`
- **Circuit Breaker Design**: See `backend/circuit_breaker.py`
- **Advanced Parallel Hybrid**: See `backend/parallel_hybrid.py`
- **API Documentation**: http://localhost:8000/docs (when running)

---

**Last Updated**: 2025-01-19  
**Version**: 2.0.0  
**Testing Infrastructure**: Week 2 Complete  

For questions or issues, refer to the troubleshooting section or check the test output for detailed error messages. 