# Branch Protection Policy

## Purpose

This document defines the recommended branch protection model for the AI-Assisted Secure SDLC project.

The goal is to ensure that changes to security automation, release logic, policies, and production-relevant code paths go through controlled review.

## Recommended Protection for `main`

The `main` branch should require:

- pull request before merge
- at least one approval
- passing AI-Assisted PR Security Review
- passing Release Security Review
- no direct pushes
- conversation resolution before merge
- CODEOWNERS review for owned paths
- signed commits where required by organization policy

## Required Status Checks

Recommended required checks:

- AI-Assisted PR Security Review
- Release Security Review

## High-Risk Change Areas

Additional review should be required for:

- `.github/workflows/`
- `ai-reviewer/`
- `policy/`
- `docs/`
- `fixtures/`
- `dashboard/`
- `monitoring/`

## Human Approval Requirements

Human approval is required for:

- production release decisions
- accepted high or critical risk
- security control changes
- CI/CD workflow changes
- secrets handling changes
- authentication or authorization changes
- Kubernetes RBAC or infrastructure permission changes

## Security Gate Behavior

If the AI-Assisted PR Security Review returns `BLOCK RECOMMENDED`, the pull request should not be merged until the issue is remediated or formally accepted by an authorized reviewer.

## Notes

This repository uses AI-assisted automation as decision support.

The automation helps identify risk, generate evidence, and improve review consistency, but it does not replace human accountability.
