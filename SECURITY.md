# Security Policy

## Reporting Security Vulnerabilities

We take the security of GitHub Green seriously. If you discover a security vulnerability, please report it responsibly.

### 🔒 How to Report

- **Email**: security@github-green.dev (if available)
- **GitHub**: Create a private security advisory
- **Direct Contact**: Message maintainers privately

### ⚡ What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fixes (if any)

### 🛡️ Security Considerations

GitHub Green is designed with security in mind:

- **No Network Requests**: All operations are local
- **No External Dependencies**: Uses only Python standard library  
- **No Credential Storage**: Relies on existing git configuration
- **Reversible Operations**: All changes can be safely undone
- **Read-Only by Default**: Only modifies specified target files

### 🔍 Security Best Practices

When using GitHub Green:

- Always backup your repository before use
- Review generated commits before pushing
- Use on private repositories for experimentation
- Don't use on repositories with sensitive data
- Keep automation logs secure (they contain commit hashes)

### 📋 Supported Versions

We provide security updates for:

| Version | Supported |
|---------|-----------|
| Latest  | ✅ Yes    |
| Previous| ⚠️ Limited|
| Older   | ❌ No     |

### 🚨 Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix & Release**: Within 30 days (for confirmed vulnerabilities)

Thank you for helping keep GitHub Green secure! 🔒
