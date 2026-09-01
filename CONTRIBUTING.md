# Contributing to FastAPI RAG Microservice

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- Be respectful and professional
- Provide constructive feedback
- Report issues privately if they involve code of conduct violations
- Collaborate in good faith

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- GitHub account
- Virtual environment knowledge

### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/fastapi-rag-microservice.git
cd fastapi-rag-microservice

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies in development mode
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Create .env file for development
cp .env.example .env
# Edit .env with your API keys
```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b bugfix/issue-number
```

Branch naming conventions:
- `feature/description` - New features
- `bugfix/issue-number` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions

### 2. Make Your Changes

```bash
# Edit files
nano config.py  # or your preferred editor

# Test your changes
python -m pytest  # If tests exist
python main.py   # Manual testing
```

### 3. Commit Your Changes

See [Commit Guidelines](#commit-guidelines) below.

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

Visit GitHub and create a PR with a clear description.

## 💬 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning (formatting, missing semicolons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Code change that improves performance
- `test`: Adding missing or correcting existing tests
- `chore`: Changes to build process, dependencies, or tools

### Example Commits

```
feat(vector-store): add support for persistent storage

- Implement PersistentClient initialization
- Add directory configuration via environment variables
- Update documentation with persistence setup

Closes #123
```

```
fix(llm-adapter): handle API timeout gracefully

When Gemini API times out, immediately fallback to Claude instead of
waiting for full timeout duration.

Closes #456
```

## 📤 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass locally
- [ ] New features include tests
- [ ] Documentation is updated
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts with main branch
- [ ] Branch is up to date with main

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #(issue number)

## Testing
Describe how you tested this change:
- [ ] Test A
- [ ] Test B

## Screenshots (if applicable)
Include screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated Checks**: GitHub Actions runs tests and linting
2. **Code Review**: Maintainers review code quality and design
3. **Feedback**: Address any requested changes
4. **Approval**: Minimum 1 approval required
5. **Merge**: Rebase and merge into main branch

## 🎨 Coding Standards

### Python Style

Follow PEP 8 with these preferences:

```python
# Good: Descriptive names, clear intent
def process_pdf_document(file_content: bytes, filename: str) -> Tuple[List[str], List[str]]:
    """Extract and chunk a PDF document."""
    text = extract_text_from_pdf(file_content)
    chunks = chunk_text(text)
    ids = generate_chunk_ids(filename, len(chunks))
    return chunks, ids

# Bad: Vague names, unclear logic
def proc(fc, fn):
    t = extr(fc)
    c = chk(t)
    i = gen(fn, len(c))
    return c, i
```

### Docstrings

Use Google-style docstrings:

```python
def add_documents(self, documents: List[str], ids: List[str], metadatas: List[Dict[str, Any]] = None) -> None:
    """
    Add documents to the vector store.

    Args:
        documents: List of text chunks to store
        ids: List of unique identifiers for each document
        metadatas: Optional list of metadata dictionaries per document

    Raises:
        ValueError: If documents and ids have different lengths

    Example:
        >>> vs = VectorStore()
        >>> vs.add_documents(['Hello world'], ['doc_1'])
    """
    pass
```

### Type Hints

Always include type hints:

```python
# Good
def query(self, query_text: str, n_results: int = None) -> Dict[str, Any]:
    pass

# Avoid
def query(self, query_text, n_results=None):
    pass
```

### Error Handling

Be specific with exceptions:

```python
# Good
try:
    response = self.client.generate_content(prompt)
except google.generativeai.APIError as e:
    raise Exception(f"Gemini API error: {str(e)}")

# Avoid
try:
    response = self.client.generate_content(prompt)
except:
    raise Exception("Error")
```

## 🧪 Testing

### Writing Tests

Tests should be in a `tests/` directory (to be created):

```python
# tests/test_document_processor.py
import pytest
from document_processor import DocumentProcessor

def test_extract_text_from_valid_pdf():
    """Test PDF text extraction with valid file."""
    processor = DocumentProcessor()
    # Test implementation
    assert result is not None

def test_chunk_text_respects_size():
    """Test that chunks don't exceed specified size."""
    processor = DocumentProcessor(chunk_size=100)
    chunks = processor.chunk_text("a" * 1000)
    for chunk in chunks:
        assert len(chunk) <= 100
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test
python -m pytest tests/test_document_processor.py::test_extract_text_from_valid_pdf

# Run with verbose output
python -m pytest -v
```

## 📚 Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update this CONTRIBUTING.md if processes change
- Include examples for new features

### API Documentation

FastAPI auto-generates docs at `/docs`. Ensure endpoints have:
- Clear description
- Parameter documentation
- Response examples

```python
@app.post("/query", response_model=ChatResponse, tags=["Chat"])
async def query_documents(request: ChatRequest):
    """
    Query the indexed documents with RAG.
    
    - **question**: User's question or query
    - **top_k**: Number of context chunks to retrieve (1-10, default 3)
    
    Returns:
        ChatResponse with answer, sources used, and model information
    """
    pass
```

## 🐛 Reporting Issues

When reporting bugs:

1. **Check existing issues** - Avoid duplicates
2. **Provide details**:
   - Python version
   - OS and Python installation method
   - Steps to reproduce
   - Error messages and stack traces
   - Expected vs actual behavior

3. **Use issue template** provided on GitHub

Example:

```markdown
## Bug Description
Brief description

## To Reproduce
1. Run `python main.py`
2. Call POST /ingest
3. Error occurs

## Environment
- Python 3.10
- Ubuntu 22.04
- FastAPI 0.104.1

## Error
```
Full traceback
```

## Expected Behavior
What should happen instead
```

## 🎯 Feature Requests

For feature requests:

1. **Check existing issues** - Avoid duplicates
2. **Provide context**:
   - Use case or problem it solves
   - Proposed solution
   - Alternatives considered
   - Examples if helpful

3. **Be specific** - Vague requests are harder to implement

Example:

```markdown
## Feature Request
Support for DOCX file ingestion in addition to PDF

## Use Case
Users with Word documents need to use the service

## Proposed Solution
- Add python-docx dependency
- Create DocumentProcessor method for DOCX extraction
- Reuse existing chunking logic

## Example Usage
curl -X POST /ingest -F "file=@document.docx"
```

## 📦 Dependency Management

### Adding Dependencies

If your changes require new dependencies:

1. Install the package: `pip install new-package`
2. Add to `requirements.txt`: `new-package==X.Y.Z`
3. Document in PR why it's needed
4. Prefer packages with:
   - Active maintenance
   - Good test coverage
   - Appropriate licenses (MIT, Apache 2.0 preferred)

### Security Considerations

- Check for known vulnerabilities: `pip install safety && safety check`
- Use pinned versions to ensure reproducibility
- Regularly update dependencies

## 🚀 Release Process

(For maintainers)

1. Update version in `__init__.py` or `setup.py`
2. Update CHANGELOG.md
3. Create release branch: `git checkout -b release/v1.0.0`
4. Create GitHub release with tag `v1.0.0`
5. Merge back to main

## 💡 Tips for Success

1. **Start small** - Contribute documentation or small fixes first
2. **Ask questions** - Open an issue to discuss before major changes
3. **Read existing code** - Understand the codebase structure
4. **Test thoroughly** - Manual and automated testing
5. **Communicate** - Clear commit messages and PR descriptions
6. **Be patient** - Reviews take time, maintainers are volunteers

## ❓ Questions?

- **GitHub Issues** - For bugs and feature requests
- **GitHub Discussions** - For questions and ideas (when available)
- **Email** - sadainsikandar506@gmail.com (for sensitive issues)

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to FastAPI RAG Microservice! 🎉

**Last Updated**: September 2024
