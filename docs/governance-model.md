# Governance Model

## Purpose

This document explains the governance model for the AI-Assisted Secure SDLC project.

The project combines automation, AI-style review logic, policy-as-code, evidence generation, and human approval gates.

## Governance Layers

| Layer | Purpose |
|---|---|
| PR Security Gate | Reviews changed files and blocks risky pull requests |
| Release Review | Checks release evidence and recommends release decision |
| Security Intelligence | Generates SARIF, risk score, and executive summary |
| Policy as Code | Defines release and approval expectations |
| CODEOWNERS | Assigns ownership for sensitive paths |
| Evidence Index | Tracks generated security evidence |
| Dashboarding | Visualizes release and security posture |

## Decision Model

| Decision | Meaning |
|---|---|
| PASS | No blocking risk detected |
| PASS WITH WARNINGS | Findings exist and require review or acceptance |
| BLOCK | High-risk issue detected and release should not proceed |

## Human Accountability

AI-assisted output is advisory.

Human reviewers remain accountable for:

- approving releases
- accepting risk
- validating false positives
- reviewing high-risk changes
- approving production deployment

## Operating Principle

The project is designed to help teams make better and faster security decisions without creating blind trust in AI-generated output.
