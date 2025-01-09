# Contributing to IntelliAgent

First off, thank you for considering contributing to IntelliAgent! It's people like you that make IntelliAgent such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include any error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and explain which behavior you expected to see instead
- Explain why this enhancement would be useful

### Pull Requests

- Fill in the required template
- Follow the Python style guide
- Include appropriate tests
- Update documentation for significant changes
- End all files with a newline

## Development Process

1. Fork the repo
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Run the linters (`./scripts/lint.sh`)
6. Commit your changes (`git commit -m 'feat: add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Create a Pull Request

## Style Guide

- Use [Black](https://github.com/psf/black) for code formatting
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Write docstrings for all public methods
- Keep functions focused and small
- Use meaningful variable names

## Git Commit Messages

- Use the present tense ("add feature" not "added feature")
- Use the imperative mood ("move cursor to..." not "moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving the format/structure of the code
  - 🐎 `:racehorse:` when improving performance
  - 📝 `:memo:` when writing docs
  - 🐛 `:bug:` when fixing a bug
  - 🔥 `:fire:` when removing code or files
  - ✅ `:white_check_mark:` when adding tests
  - 🔒 `:lock:` when dealing with security

## Additional Notes

### Issue and Pull Request Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation only changes
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

Thank you for contributing to IntelliAgent! 🎉
