# QA Automation — Hacking Harness

This directory contains browser-based security validation for pentesting
targets being audited with this harness.

## Structure

```
qa/
├── qa-runner.mjs           # Generic Playwright test runner
├── qa-security.mjs          # Security validation (XSS, CSRF, headers, cookies)
├── setup-qa-local.sh        # Environment setup script
├── qa-reports/              # Generated reports and screenshots
│   └── screenshots/
└── README.md                # This file
```

## Prerequisites

- Node.js 18+
- npm

## Setup

```bash
bash qa/setup-qa-local.sh
```

This installs Playwright and Chromium, then creates the reports directory.

## Usage

```bash
# Security validation against a target
node qa/qa-security.mjs --url https://target.com

# With environment variable
APP_URL=https://target.com node qa/qa-security.mjs
```

## Available Tests

| Test | Description |
|------|-------------|
| `qa-security.mjs` | Full security validation: XSS, CSRF, headers, cookies, clickjacking |

## Security Test Coverage

- XSS Reflected protection
- CSP, HSTS, X-Frame-Options headers
- Cookie security flags (HttpOnly, Secure, SameSite)
- Clickjacking protection (X-Frame-Options / CSP frame-ancestors)
- Information disclosure via Server header
- Cross-Origin Resource Sharing (CORS)

## Adding New Tests

1. Create a new function in `qa-security.mjs` following the existing pattern
2. Register it in the main flow
3. Add acceptance criteria in `task-qa-browser.md`

## Configuration

| Arg | Default | Description |
|-----|---------|-------------|
| `APP_URL` | `http://localhost:5000` | Base URL of the target |
| `REPORT_DIR` | `qa/qa-reports/` | Output directory |
