# Contributing to Helix Orchestration

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the Helix Orchestration project.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and the expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python styleguides
- Include appropriate test cases
- End all files with a newline
- Avoid platform-dependent code

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- pip or uv

### Local Development

1. **Fork the repository**
   ```bash
   gh repo fork Deathcharge/helix-hub-agents --clone
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/helix_orchestration

# Run specific test file
pytest tests/test_agent_orchestrator.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Lint with ruff
ruff check src/ tests/

# Type checking with mypy
mypy src/

# Run all checks
pre-commit run --all-files
```

## Styleguides

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

### Example Function

```python
def orchestrate_agents(
    agents: List[Agent],
    task: str,
    context: Optional[Dict[str, Any]] = None,
    timeout: int = 300
) -> OrchestratedResult:
    """
    Orchestrate multiple agents to complete a task.
    
    Args:
        agents: List of agents to coordinate
        task: Task description
        context: Optional context data
        timeout: Execution timeout in seconds
        
    Returns:
        OrchestratedResult containing execution results and metrics
        
    Raises:
        TimeoutError: If execution exceeds timeout
        ValueError: If task or agents are invalid
    """
    # Implementation
    pass
```

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add agent emergence simulation

- Implement predictive modeling for agent behavior
- Add tests for emergence patterns
- Update documentation with examples

Fixes #123
```

### Documentation

- Use clear, concise language
- Include code examples where appropriate
- Update README.md if adding new features
- Add docstrings to all public APIs
- Keep documentation up-to-date with code changes

## Testing Guidelines

### Test Structure

```python
import pytest
from helix_orchestration import AgentOrchestrator

class TestAgentOrchestrator:
    """Test suite for AgentOrchestrator"""
    
    @pytest.fixture
    def orchestrator(self):
        """Fixture providing orchestrator instance"""
        return AgentOrchestrator()
    
    def test_agent_registration(self, orchestrator):
        """Test that agents can be registered"""
        agent = orchestrator.registry.get_agent("kael")
        assert agent is not None
        assert agent.name == "kael"
    
    @pytest.mark.asyncio
    async def test_async_orchestration(self, orchestrator):
        """Test async orchestration"""
        result = await orchestrator.execute_async(
            agents=["kael", "lumina"],
            task="test_task"
        )
        assert result.success
```

### Coverage Requirements

- Aim for >80% code coverage
- All public APIs must have tests
- Test both success and failure cases
- Include edge cases and boundary conditions

## Documentation

### Adding Documentation

1. Create a new file in `docs/` directory
2. Use Markdown format
3. Include code examples
4. Update `docs/index.md` with link to new documentation

### Documentation Structure

```markdown
# Feature Name

## Overview
Brief description of the feature.

## Use Cases
When and why to use this feature.

## Examples

### Basic Example
```python
# Code example
```

### Advanced Example
```python
# More complex example
```

## API Reference
Detailed API documentation.

## See Also
Links to related documentation.
```

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a release branch: `git checkout -b release/v1.0.0`
4. Create a pull request
5. After merge, create a GitHub release
6. Package will be automatically published to PyPI

## Questions?

- Open an issue with the `question` label
- Start a discussion in GitHub Discussions
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to Helix Orchestration! 🎉
