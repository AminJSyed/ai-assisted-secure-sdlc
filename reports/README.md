# Generated Reports

This directory is used for runtime-generated Secure SDLC reports.

The generated report files are intentionally not committed to Git.

Reports are produced locally and in GitHub Actions, then uploaded as workflow artifacts.

Typical generated files include:

| Report | Purpose |
|---|---|
| ai-assisted-security-review.md | AI-assisted PR/code security review |
| finding-triage-report.md | Vulnerability triage summary |
| release-security-review.md | Release readiness decision |
| executive-release-summary.md | Executive release security summary |
| security-risk-score.md | Risk score and recommended decision |
| ai-assisted-remediation-plan.md | AI-assisted remediation plan |
| ai-assisted-findings.sarif | SARIF output for GitHub Code Scanning |

To generate reports locally:

    make all

To view reports from CI:

    GitHub Actions -> workflow run -> Artifacts

SARIF findings are visible under:

    Security and quality -> Code scanning
