// qa-security.mjs — Security validation tests for Hacking Harness
// Tests XSS, CSRF, security headers, cookies, clickjacking

import { chromium } from 'playwright';

const BASE_URL = process.env.APP_URL || 'http://localhost:5000';
const REPORT_DIR = process.env.REPORT_DIR || 'qa/qa-reports';

const results = [];
const errors = [];

function logResult(name, passed, details = '') {
  results.push({ name, passed, details });
  const status = passed ? '\x1b[32mPASS\x1b[0m' : '\x1b[31mFAIL\x1b[0m';
  console.log(`  [${status}] ${name}${details ? ' - ' + details : ''}`);
}

async function takeScreenshot(page, name) {
  const fs = await import('fs');
  const dir = `${REPORT_DIR}/screenshots`;
  fs.mkdirSync(dir, { recursive: true });
  await page.screenshot({ path: `${dir}/${name}.png`, fullPage: true });
}

async function testSecurityHeaders(url) {
  console.log('\n── Security Headers Test ──');
  try {
    const response = await fetch(url);
    const headers = response.headers;

    logResult('Strict-Transport-Security (HSTS)',
      headers.has('strict-transport-security'),
      headers.get('strict-transport-security') || 'missing'
    );

    logResult('X-Frame-Options',
      headers.has('x-frame-options'),
      headers.get('x-frame-options') || 'missing'
    );

    logResult('X-Content-Type-Options',
      headers.has('x-content-type-options'),
      headers.get('x-content-type-options') || 'missing'
    );

    logResult('Content-Security-Policy',
      headers.has('content-security-policy'),
      headers.get('content-security-policy') || 'missing'
    );

    logResult('X-XSS-Protection',
      headers.has('x-xss-protection'),
      headers.get('x-xss-protection') || 'missing'
    );

    logResult('Referrer-Policy',
      headers.has('referrer-policy'),
      headers.get('referrer-policy') || 'missing'
    );

    logResult('Server header present (information disclosure)',
      !headers.has('server') || headers.get('server') === '',
      headers.get('server') || 'hidden/removed'
    );
  } catch (err) {
    console.error(`  Error testing headers: ${err.message}`);
    errors.push(`headers: ${err.message}`);
  }
}

async function testXSS(page, url) {
  console.log('\n── XSS Basic Test ──');
  try {
    const testPayload = '<script>alert("XSS-TEST")</script>';
    const testUrl = `${url}/search?q=${encodeURIComponent(testPayload)}`;

    const consoleErrors = [];
    page.on('console', msg => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });

    await page.goto(testUrl, { waitUntil: 'networkidle', timeout: 10000 });
    await takeScreenshot(page, 'xss-test');

    const html = await page.content();
    const xssDetected = html.includes(testPayload) && !html.includes('&lt;script&gt;');

    logResult('XSS Reflected Protection',
      !xssDetected,
      xssDetected ? 'Payload not sanitized!' : 'Payload sanitized/escaped'
    );

    if (consoleErrors.length > 0) {
      console.log(`  Console errors: ${consoleErrors.join(', ')}`);
    }
  } catch (err) {
    console.error(`  Error testing XSS: ${err.message}`);
    errors.push(`xss: ${err.message}`);
  }
}

async function testClickjacking(page, url) {
  console.log('\n── Clickjacking Test ──');
  try {
    // Test via X-Frame-Options was done in headers test
    // Additional test: verify CSP frame-ancestors
    const response = await fetch(url);
    const csp = response.headers.get('content-security-policy') || '';
    const hasFrameAncestors = csp.includes('frame-ancestors');

    logResult('CSP frame-ancestors',
      hasFrameAncestors,
      hasFrameAncestors ? csp.split(';').find(s => s.includes('frame-ancestors')).trim() : 'missing'
    );
  } catch (err) {
    console.error(`  Error testing clickjacking: ${err.message}`);
    errors.push(`clickjacking: ${err.message}`);
  }
}

async function testCookies(page, url) {
  console.log('\n── Cookie Security Test ──');
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 10000 });
    const cookies = await page.context().cookies();

    for (const cookie of cookies) {
      console.log(`  Cookie: ${cookie.name}`);
      logResult(`HttpOnly (${cookie.name})`,
        cookie.httpOnly,
        cookie.httpOnly ? 'Yes' : 'No'
      );
      logResult(`Secure (${cookie.name})`,
        cookie.secure,
        cookie.secure ? 'Yes' : 'No'
      );
      logResult(`SameSite (${cookie.name})`,
        cookie.sameSite !== 'None' && cookie.sameSite !== 'none',
        cookie.sameSite || 'not set'
      );
    }

    if (cookies.length === 0) {
      logResult('Cookies present', false, 'No cookies found');
    }
  } catch (err) {
    console.error(`  Error testing cookies: ${err.message}`);
    errors.push(`cookies: ${err.message}`);
  }
}

async function generateReport() {
  const fs = await import('fs');
  const passed = results.filter(r => r.passed).length;
  const failed = results.filter(r => !r.passed).length;
  const total = results.length;
  const score = total > 0 ? Math.round((passed / total) * 100) : 0;

  const report = `
## QA Browser Security Report
**Fecha:** ${new Date().toISOString().split('T')[0]}
**URL testeada:** ${BASE_URL}

### Security Score
| Categoría | Score |
|-----------|-------|
| Total Tests | ${total} |
| Passed | ${passed} |
| Failed | ${failed} |
| **Security Score** | **${score}/100** |

### Results
${results.map(r => `| ${r.name} | ${r.passed ? '✅' : '❌'} | ${r.details} |`).join('\n')}

### Errors
${errors.length > 0 ? errors.map(e => `- ${e}`).join('\n') : 'None'}

### Screenshots
- \`qa/qa-reports/screenshots/\`
`;

  const reportPath = `${REPORT_DIR}/security-report.md`;
  fs.mkdirSync(REPORT_DIR, { recursive: true });
  fs.writeFileSync(reportPath, report.trim());
  console.log(`\nReport saved: ${reportPath}`);
}

async function main() {
  console.log('═══════════════════════════════════════════');
  console.log('  QA BROWSER - Security Validation');
  console.log(`  Target: ${BASE_URL}`);
  console.log('═══════════════════════════════════════════');

  // Test security headers first (no browser needed)
  await testSecurityHeaders(BASE_URL);

  // Browser-based tests
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  const page = await context.newPage();

  try {
    await testXSS(page, BASE_URL);
    await testClickjacking(page, BASE_URL);
    await testCookies(page, BASE_URL);
  } finally {
    await browser.close();
  }

  await generateReport();

  console.log('\n═══════════════════════════════════════════');
  const failedCount = results.filter(r => !r.passed).length;
  if (failedCount > 0) {
    console.log(`  ⚠️  ${failedCount} security test(s) FAILED`);
    process.exit(1);
  } else {
    console.log('  ✅ All security tests PASSED');
  }
  console.log('═══════════════════════════════════════════');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
