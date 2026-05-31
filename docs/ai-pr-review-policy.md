# AI-Assisted PR Review Policy

## Purpose

This policy defines how AI-assisted PR security review should be used.

## What the Reviewer Checks

The reviewer checks for:

- hardcoded secrets
- SQL injection patterns
- command injection patterns
- unsafe HTML rendering
- weak authentication patterns
- insecure Dockerfile configuration
- insecure Kubernetes manifests
- missing resource limits
- missing securityContext
- missing health checks
- risky CI/CD changes

## Advisory Nature

The AI-assisted review is advisory.

It does not automatically approve a pull request.

## Required Human Approval

Human approval is required for:

- authentication changes
- authorization changes
- secrets handling
- CI/CD deployment changes
- production configuration
- infrastructure permissions
- payment or financial logic
- Kubernetes RBAC changes
- security control changes

## Pull Request Decision

| Decision | Meaning |
|---|---|
| PASS | No risky pattern detected |
| REVIEW REQUIRED | Potential risk needs human review |
| BLOCK RECOMMENDED | High-risk pattern detected |
