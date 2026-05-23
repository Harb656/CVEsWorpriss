# 🤝 Contributing to InMyMine7

Thank you for your interest in contributing to InMyMine7! This document provides guidelines and instructions for contributing to the project.

## ⚠️ Legal & Ethical Guidelines

**IMPORTANT:** This tool is intended **ONLY** for authorized penetration testing and security research.

By contributing to this project, you agree that:

1. ✅ You understand this tool is for authorized testing only
2. ✅ You will not use or contribute code that enables unauthorized access
3. ✅ You will respect laws and regulations in your jurisdiction
4. ✅ You will not help others misuse this tool
5. ✅ You understand the author assumes no liability for misuse

## 🐛 Reporting Bugs

### Before Reporting

1. Check the [README](../README.md) for common issues
2. Search [existing issues](https://github.com/InMyMine7/InMyMine7/issues)
3. Check [Discussions](https://github.com/InMyMine7/InMyMine7/discussions)

### How to Report

1. Use the [Bug Report template](ISSUE_TEMPLATE/bug_report.md)
2. Include as much detail as possible:
   - Operating system and version
   - Python version
   - Tool version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error logs/screenshots

### For Security Vulnerabilities

**DO NOT** create a public issue for security vulnerabilities!

Instead:
- Contact [@InMyMineee](https://t.me/InMyMineee) on Telegram
- Email: [if email is provided]
- Use the private security advisory feature on GitHub

## ✨ Suggesting Features

### Before Suggesting

1. Check [existing feature requests](https://github.com/InMyMine7/InMyMine7/issues?q=label%3Aenhancement)
2. Ensure the feature aligns with the project's purpose

### How to Suggest

1. Use the [Feature Request template](ISSUE_TEMPLATE/feature_request.md)
2. Describe:
   - What problem does this solve?
   - How would users interact with this feature?
   - Are there alternatives?
   - Any examples or mockups?

## 💻 Code Contributions

### Getting Started

1. **Fork** the repository
2. **Clone** your fork:
```bash
git clone https://github.com/YOUR-USERNAME/InMyMine7.git
cd ExWP
```

3. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

### Coding Standards

#### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation
- Keep lines under 100 characters when possible
- Use meaningful variable and function names

#### Documentation
- Add docstrings to all functions and classes
- Include comments for complex logic
- Update README if adding new features

#### Example:
```python
def check_file(self, filename):
    """
    Check if a required file exists in the configured directory.
    
    Args:
        filename (str): Name of the file to check
        
    Returns:
        bool: True if file exists, False otherwise
    """
    file_path = os.path.join(self.CONFIG['FILES_DIR'], filename)
    if not os.path.exists(file_path):
        self.log_message(f"File {filename} not found", error=True)
        return False
    return True
```

#### Error Handling
- Always handle exceptions appropriately
- Log errors with meaningful messages
- Don't silently fail

### Adding New Exploits

#### File Structure
```
lib/tools/exploit_CVE_XXXX_XXXX.py
```

#### Template
```python
"""
Exploit for CVE-XXXX-XXXX
Description: Brief description of the vulnerability
"""

def exploit_cve_xxxx_xxxx(url, session, headers, proxies, config):
    """
    Exploit the vulnerability.
    
    Args:
        url (str): Target URL
        session (requests.Session): HTTP session
        headers (dict): HTTP headers
        proxies (dict): Proxy configuration
        config (dict): Configuration dictionary
        
    Returns:
        dict: Results containing success status and data
    """
    try:
        # Implementation here
        return {
            'success': True,
            'message': 'Exploitation successful',
            'data': results
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}',
            'data': None
        }
```

#### Registration
Add your exploit to `production.py`:
```python
EXPLOITS = {
    # ... existing exploits ...
    'CVE_XXXX_XXXX': 'lib.tools.exploit_cve_xxxx_xxxx.exploit_cve_xxxx_xxxx',
}
```

### Testing Your Changes

1. **Manual Testing:**
```bash
python production.py
```

2. **Test on Different Platforms:**
   - Windows
   - Linux (Ubuntu, Fedora, Arch)
   - macOS

3. **Test with Different Python Versions:**
   - Python 3.8
   - Python 3.9
   - Python 3.10+

4. **Code Quality:**
```bash
# Check for common issues
python -m py_compile production.py lib/tools/*.py
```

### Submitting Changes

1. **Commit with Clear Messages:**
```bash
git commit -m "Add feature: brief description"
```

2. **Push to Your Fork:**
```bash
git push origin feature/your-feature-name
```

3. **Create a Pull Request:**
   - Use the [PR template](PULL_REQUEST_TEMPLATE.md)
   - Link related issues
   - Describe changes clearly
   - Include testing information

## 📚 Documentation Contributions

### Improving Documentation

1. Check the [Documentation template](ISSUE_TEMPLATE/documentation.md)
2. Focus areas:
   - README improvements
   - Installation guide clarifications
   - Usage examples
   - Troubleshooting guides
   - Comments in code

### Writing Good Documentation

- Use clear, simple language
- Include examples
- Add step-by-step instructions
- Provide expected outputs
- Include troubleshooting tips

## 🚀 Pull Request Process

1. **Ensure your PR:**
   - ✅ Passes all checks
   - ✅ Follows code style
   - ✅ Includes tests
   - ✅ Updates documentation
   - ✅ Uses the PR template

2. **Wait for review:**
   - Be responsive to feedback
   - Make requested changes
   - Re-request review when ready

3. **Merge:**
   - PR will be merged by maintainer
   - Your contribution will be credited

## 💬 Communication

### Where to Discuss

- **Issues:** Bug reports and feature requests
- **Discussions:** Questions and general chat
- **Telegram:** Quick questions and support
- **Email:** For sensitive matters

### Be Respectful

- Use respectful language
- Assume good intentions
- Help others learn
- Don't spam or promote unrelated content

## 🏆 Recognition

Contributors will be recognized in:
- Pull request comments
- Release notes
- Contributors list (if applicable)

## 📋 Checklist Before Submitting

- [ ] Code follows PEP 8 style guide
- [ ] Changes are tested
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No sensitive information included
- [ ] Changes align with project goals
- [ ] PR description is complete
- [ ] Related issues are linked

## ❓ Questions?

- Open a [Discussion](https://github.com/InMyMine7/InMyMine7/discussions)
- Message [@InMyMineee](https://t.me/InMyMineee) on Telegram
- Check the [README](../README.md)

---

**Thank you for contributing to InMyMine7!** 🙏

Your contributions help make this tool better for the security community while maintaining ethical standards.

**Remember:** This tool is only for authorized penetration testing. Use it responsibly and legally.
