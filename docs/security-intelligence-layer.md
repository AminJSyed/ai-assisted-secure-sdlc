# Security Intelligence Layer

## Purpose

The Security Intelligence Layer converts AI-assisted security review output into structured security evidence.

It adds:

- SARIF output for GitHub Code Scanning
- executive release summary
- security risk score
- AI-style remediation guidance
- advisory release decision support

## Generated Reports

| Report | Purpose |
|---|---|
| reports/ai-assisted-findings.sarif | SARIF file for GitHub Code Scanning |
| reports/security-risk-score.md | Risk score and recommended decision |
| reports/executive-release-summary.md | Executive release security summary |

## SARIF Integration

SARIF allows AI-assisted findings to appear in GitHub Code Scanning.

This makes the workflow closer to enterprise AppSec tooling because findings can be reviewed in GitHub Security views.

## Risk Scoring

The risk score is calculated using rule weights.

High-risk issues such as SQL injection and command injection contribute more to the score.

The score is advisory and must be validated by a human reviewer.

## Human Approval

The Security Intelligence Layer does not approve releases automatically.

It provides structured decision support for security engineers, developers, and release managers.
