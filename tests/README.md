# Vidalytics Testing Infrastructure

Comprehensive testing framework for the Vidalytics YouTube Analytics platform.

## 🚀 Quick Start

### Prerequisites
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx fastapi

# Optional for enhanced features
pip install pytest-xdist pytest-html pytest-benchmark
```

### Running Tests

#### Interactive Menu
```bash
python tests/run_tests.py
```
Choose from:
1. Quick smoke test
2. Full test suite with coverage
3. Check dependencies 
4. Unit tests only
5. Integration tests only
6. Custom options

#### Command Line Options
```bash
# Run all tests
python tests/run_tests.py --type all --verbose

# Unit tests only
python tests/run_tests.py --type unit --coverage

# Integration tests with parallel execution
python tests/run_tests.py --type integration --parallel

# Run specific file
python tests/run_tests.py --file unit/test_youtube_analytics_service.py

# Fast mode (skip slow tests)
python tests/run_tests.py --type all --fast
```

#### Direct pytest Usage
```bash
# Run with markers
pytest -m unit -v
pytest -m integration --cov=backend
pytest -m "not slow" -x

# Run specific test
pytest tests/unit/test_youtube_analytics_service.py::TestYouTubeAnalyticsService::test_initialization -v
```

## 📁 Test Structure

```
tests/
├── conftest.py                 # Global fixtures and configuration
├── run_tests.py               # Test runner with interactive menu
├── pytest.ini                # Pytest configuration (in root)
├── fixtures/                  # Test data and mock objects
│   ├── sample_data.py        # General test data factory
│   └── youtube_analytics_fixtures.py  # YouTube-specific fixtures
├── unit/                     # Unit tests for individual components
│   ├── test_youtube_analytics_service.py
│   ├── test_boss_agent.py
│   └── ...
├── integration/              # Integration tests between components
│   ├── test_analytics_endpoints.py
│   ├── test_agent_coordination.py
│   └── ...
├── e2e/                     # End-to-end workflow tests
│   └── test_user_workflows.py
├── security/                # Security-focused tests
│   └── test_security.py
└── utils/                   # Test utilities and helpers
    ├── test_database.py     # Database test utilities
    └── __init__.py
```

## 🏷️ Test Categories & Markers

### Test Markers
- `@pytest.mark.unit` - Unit tests for individual components
- `@pytest.mark.integration` - Integration tests between components
- `@pytest.mark.e2e` - End-to-end workflow tests
- `@pytest.mark.security` - Security-focused tests
- `@pytest.mark.performance` - Performance and load tests
- `@pytest.mark.slow` - Tests taking >5 seconds
- `@pytest.mark.asyncio` - Async tests

### Running by Marker
```bash
pytest -m unit                    # Unit tests only
pytest -m "integration or e2e"    # Integration and E2E tests
pytest -m "not slow"              # Skip slow tests
```

## 🧪 Test Types Explained

### Unit Tests
Test individual components in isolation with mocked dependencies.

**Examples:**
- `test_youtube_analytics_service.py` - YouTube Analytics Service methods
- `test_boss_agent.py` - Boss Agent functionality and delegation
- Component validation, error handling, data processing

**Key Features:**
- Fast execution (<1s per test)
- Isolated with mocked external dependencies
- High coverage of edge cases and error scenarios

### Integration Tests  
Test interaction between multiple components and services.

**Examples:**
- `test_analytics_endpoints.py` - API endpoints with service integration
- `test_agent_coordination.py` - Boss Agent + Specialist Agent workflows
- Database operations with real connections

**Key Features:**
- Test complete request/response flows
- Verify component interactions
- Use test databases and mock external APIs

### End-to-End Tests
Test complete user workflows from start to finish.

**Examples:**
- User authentication → Dashboard → Analytics request → Response
- OAuth flow → Channel connection → Data retrieval

**Key Features:**
- Simulate real user interactions
- Test complete system integration
- Higher execution time but comprehensive validation

## 🛠️ Test Utilities

### Test Database Manager
```python
from tests.utils import get_test_db_manager, TestDataFactory

# Create test database with sample data
db_manager = get_test_db_manager()
with db_manager.database_session() as conn:
    db_manager.setup_test_tables(conn)
    test_data = TestDataFactory.create_complete_test_dataset()
    db_manager.insert_test_data(conn, test_data)
```

### Fixtures Available
- `test_settings` - Test configuration
- `mock_env_vars` - Environment variable mocking
- `test_client` - FastAPI test client
- `async_client` - Async HTTP client
- `mock_openai` - OpenAI API mocking
- `mock_youtube_api` - YouTube API mocking
- `test_database` - Clean test database
- `test_database_with_data` - Pre-populated test database

### Sample Data Factory
```python
from tests.fixtures.sample_data import SampleDataFactory

# Create test data
user_data = SampleDataFactory.create_user_data("test-user-123")
video_data = SampleDataFactory.create_video_data("test-video-456")
analytics_data = SampleDataFactory.create_channel_analytics()
```

## 📊 Coverage Reporting

### HTML Reports
```bash
python tests/run_tests.py --coverage
# View: htmlcov/index.html
```

### Terminal Reports
Coverage is shown in terminal with missing lines highlighted.

### Coverage Thresholds
- Minimum: 80% overall coverage
- Unit tests: Aim for >90% coverage
- Integration tests: Focus on critical paths

### Coverage Configuration
Set in `pytest.ini`:
```ini
[coverage:run]
source = backend
omit = */tests/*, */venv/*, */__pycache__/*

[coverage:report]
show_missing = true
skip_covered = false
```

## 🚨 Error Handling & Debugging

### Common Issues

#### Import Errors
```bash
# If modules not found, ensure PYTHONPATH is set
export PYTHONPATH=/path/to/Vidalytics/backend:$PYTHONPATH
```

#### Async Test Issues
```python
# Use pytest.mark.asyncio for async tests
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

#### Database Connection Issues
```python
# Use test database fixtures
def test_with_db(test_database):
    conn, db_path = test_database
    # Test with clean database
```

### Debug Mode
```bash
# Run with pdb debugger
pytest --pdb

# Stop on first failure
pytest -x

# Verbose output with full tracebacks
pytest -vvv --tb=long
```

## ⚡ Performance Testing

### Benchmark Tests
```python
@pytest.mark.performance
def test_performance_benchmark(benchmark):
    result = benchmark(function_to_test)
    assert result is not None
```

### Load Testing
```python
@pytest.mark.performance
@pytest.mark.slow
async def test_concurrent_requests():
    # Test handling multiple simultaneous requests
    tasks = [make_request() for _ in range(100)]
    results = await asyncio.gather(*tasks)
```

## 🔐 Security Testing

### Security Test Categories
- Input validation and sanitization
- Authentication and authorization
- Rate limiting and abuse prevention
- SQL injection prevention
- XSS protection
- CSRF protection

### Example Security Test
```python
@pytest.mark.security
async def test_sql_injection_protection(async_client):
    # Test malicious input is properly sanitized
    malicious_input = "'; DROP TABLE users; --"
    response = await async_client.get(f"/api/search?q={malicious_input}")
    assert response.status_code != 500
```

## 🚀 Continuous Integration

### GitHub Actions Integration
Test runner is designed to work with CI/CD pipelines:

```yaml
# Example .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements-test.txt
      - name: Run tests
        run: python tests/run_tests.py --type all --coverage
```

### Pre-commit Hooks
```bash
# Run quick tests before commits
python tests/run_tests.py --fast
```

## 📈 Test Metrics & Monitoring

### Key Metrics
- Test execution time per category
- Coverage percentage by module
- Test success rate over time
- Performance regression detection

### Reporting
- HTML coverage reports: `htmlcov/index.html`
- XML coverage for CI: `coverage.xml`
- JSON test results: `test-report.json`
- HTML test results: `test-report.html`

## 🛡️ Best Practices

### Writing Tests
1. **Descriptive Names**: Test names should describe what they verify
2. **Arrange-Act-Assert**: Structure tests clearly
3. **Independence**: Tests should not depend on each other
4. **Mocking**: Mock external dependencies in unit tests
5. **Edge Cases**: Test boundary conditions and error scenarios

### Test Organization
1. **One Concept Per Test**: Each test should verify one specific behavior
2. **Proper Markers**: Use appropriate pytest markers
3. **Fixtures**: Use fixtures for common setup/teardown
4. **Data Separation**: Keep test data separate from test logic

### Performance
1. **Fast Unit Tests**: Unit tests should run quickly (<1s each)
2. **Parallel Execution**: Use pytest-xdist for parallel test execution
3. **Test Selection**: Use markers to run only relevant tests during development
4. **Resource Cleanup**: Ensure proper cleanup to prevent resource leaks

## 🔧 Troubleshooting

### Common Test Failures
1. **Import Errors**: Check PYTHONPATH and module installation
2. **Async Issues**: Ensure proper async/await usage and event loop handling
3. **Mock Issues**: Verify mock setup and reset between tests
4. **Database Issues**: Use test database fixtures and ensure cleanup

### Getting Help
1. Run dependency check: `python tests/run_tests.py` → Option 3
2. Check pytest configuration: `pytest --collect-only`
3. Run with maximum verbosity: `pytest -vvv --tb=long`
4. Review test logs and error messages carefully

---

## 📝 Development Workflow

1. **Write failing test first** (TDD approach)
2. **Implement minimum code** to make test pass
3. **Refactor** while keeping tests green
4. **Run relevant test subset** during development
5. **Run full suite** before committing
6. **Check coverage** to identify untested code
7. **Add integration tests** for new features
8. **Update documentation** as needed

This testing infrastructure ensures reliable, maintainable code with comprehensive validation of all system components.