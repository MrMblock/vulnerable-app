# Vulnerable Test Application

A deliberately vulnerable web application for testing security scanners.

**WARNING: This application contains intentional security vulnerabilities. Do NOT deploy in production.**

## Stack
- Backend: Python (Flask)
- Frontend: Node.js (Express)
- Database: SQLite / PostgreSQL

## Vulnerabilities included
- SQL Injection
- Cross-Site Scripting (XSS)
- Hardcoded secrets & API keys
- Insecure dependencies
- Command injection
- Path traversal
- Insecure deserialization
- SSRF
- Weak cryptography
- Missing security headers

## Setup
```bash
pip install -r requirements.txt
npm install
python app.py
```
# Monitoring test - 2026-03-23T13:01:35Z
