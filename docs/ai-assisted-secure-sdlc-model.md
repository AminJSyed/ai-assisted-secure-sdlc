# AI-Assisted Secure SDLC Model

## Purpose

This document describes the operating model for AI-assisted security review across the Secure SDLC.

## Core Idea

AI-assisted security engineering helps security teams and development teams review changes faster and more consistently.

It should provide decision support, not autonomous approval for high-risk changes.

## Secure SDLC Stages

| Stage | Security Activity | AI-Assisted Support |
|---|---|---|
| Requirements | Define security expectations | Suggest security requirements and abuse cases |
| Design | Threat modeling | Highlight trust boundaries and risky flows |
| Development | Secure coding | Review code for insecure patterns |
| Pull Request | Security review | Summarize risky changes and recommended checks |
| Build | Automated scanning | Interpret SAST, SCA, secrets, container, and IaC output |
| Test | DAST and integration testing | Summarize findings and retest needs |
| Release | Release readiness | Generate pass, warning, or block recommendation |
| Operations | Monitoring and response | Summarize evidence and incident signals |

## Guardrails

AI-assisted security workflows must include:

- human approval for high-risk changes
- no real secrets in prompts
- least-privilege access
- audit logs
- explainable recommendations
- scan result validation
- false-positive review
- clear release criteria

## Decision Categories

| Decision | Meaning |
|---|---|
| PASS | No blocking risks found |
| PASS WITH WARNINGS | Risks exist but can be accepted or tracked |
| BLOCK | High-risk issue requires remediation before release |

## Example Use Cases

- Review a pull request for insecure code patterns
- Summarize SAST and dependency findings
- Check Dockerfile and Kubernetes hardening
- Generate release readiness evidence
- Suggest remediation steps
- Highlight missing security gates
