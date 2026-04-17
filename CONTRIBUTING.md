# Contributing to Trumpet Cloud Backend

First off, thank you for considering contributing to Trumpet Cloud Backend! 

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setting Up Your Development Environment](#setting-up-your-development-environment)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Style Guides](#style-guides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [Documentation Style Guide](#documentation-style-guide)
- [Project Structure](#project-structure)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inclusive environment. By participating, you are expected to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+**
- **Poetry** (for dependency management)
- **PostgreSQL** (for local database)
- **Docker** and **Docker Compose** (optional, for containerized development)
- **Git**

### Setting Up Your Development Environment

1. **Fork the repository**
   
   Click the "Fork" button at the top right of the repository page.

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/trumpet-cloud-backend.git
   cd trumpet-cloud-backend
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/tvsltd-healthcare/trumpet-cloud-backend.git
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your local configuration
   ```

5. **Configure GitHub authentication for private dependencies**
   
   This project uses private GitHub packages. See the [Private Dependencies](#private-dependencies) section in the README for setup instructions.

6. **Install dependencies**
   ```bash
   poetry install
   ```

7. **Set up the database**
   ```bash
   psql -U postgres -c "CREATE DATABASE trumpet_dev;"
   ```

8. **Run the application**
   ```bash
   poetry shell
   ./entrypoint.sh
   ```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible.

**How to submit a bug report:**

1. Go to the [Issues](https://github.com/tvsltd-healthcare/trumpet-cloud-be/issues) page
2. Click "New Issue"
3. Use the bug report template (if available) or include:
   - **Clear title** describing the issue
   - **Steps to reproduce** the behavior
   - **Expected behavior** vs **actual behavior**
   - **Environment details** (OS, Python version, etc.)
   - **Screenshots or logs** if applicable
   - **Possible solution** (if you have one)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title** describing the enhancement
- **Detailed description** of the proposed functionality
- **Use case** explaining why this enhancement would be useful
- **Possible implementation** approach (optional)

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:

- `good first issue` - Simple issues ideal for newcomers
- `help wanted` - Issues that need attention
- `documentation` - Documentation improvements

### Pull Requests

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make your changes**
   - Write clear, readable code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   poetry run pytest
   
   # Run linting
   poetry run flake8
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Keep your branch updated**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template with:
     - Description of changes
     - Related issue number (if applicable)
     - Screenshots (if applicable)
     - Checklist of completed items

## Style Guides

### Git Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)

**Examples:**
```bash
feat(auth): add JWT token refresh endpoint
fix(database): resolve connection pool exhaustion
docs(readme): update installation instructions
```

### Python Style Guide

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints where appropriate
- Write docstrings for all public functions and classes



### Documentation Style Guide

- Use clear, concise language
- Include code examples where helpful
- Keep README and documentation up to date with code changes
- Use Markdown formatting consistently

## Project Structure

```plaintext
.
├── adapters/           
├── application_layer/                   
├── domain_layer/           # Domain logics
├── main.py 
├── app_layer_entrypoint.py  
├── pyproject.toml          # Poetry dependencies
└── README.md               # Project README
```

## Community

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Pull Requests**: All contributions are welcome!

---

Thank you for contributing to Trumpet Cloud Backend! 🎺
