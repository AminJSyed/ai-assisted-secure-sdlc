# AI-Assisted Secure SDLC

AI-assisted security review, vulnerability triage, and release readiness automation for secure software delivery.

## Purpose

This project demonstrates how AI-assisted engineering can support Secure SDLC workflows.

It focuses on using automation and AI-style review logic to support:

- pull request security review
- secure code review
- vulnerability triage
- release readiness checks
- secure software release management
- security evidence generation
- human approval gates

This project does not replace human review.

The goal is to support security engineers, developers, and release managers with structured security decision support.

## What This Project Demonstrates

This project demonstrates:

- AI-assisted PR security review
- AI-assisted secure code review
- AI-assisted vulnerability triage
- AI-assisted release readiness review
- AI-assisted security evidence generation
- Secure SDLC workflow automation
- advisory security gates
- human approval policy for high-risk changes

## Current Design

The first version uses a local rule-based AI-style reviewer.

This avoids the need for a real LLM API key and makes the project safe to run in CI/CD.

Future versions can optionally integrate with an LLM provider through a protected secret.

## Secure SDLC Flow

| Stage | AI-Assisted Activity |
|---|---|
| Planning | Identify security requirements and approval needs |
| Development | Review code patterns, secrets, dependencies, and configs |
| Pull Request | Generate AI-assisted security review summary |
| Build | Check SAST, SCA, container, and IaC evidence |
| Release | Generate release readiness decision |
| Production Readiness | Require human approval for risky changes |
| Evidence | Produce markdown security evidence and review reports |

## Project Structure

    ai-assisted-secure-sdlc/
    |
    |-- README.md
    |-- Makefile
    |
    |-- ai-reviewer/
    |   |-- review_changed_files.py
    |   |-- release_security_review.py
    |   |-- finding_triage_assistant.py
    |
    |-- docs/
    |   |-- ai-assisted-secure-sdlc-model.md
    |   |-- ai-pr-review-policy.md
    |   |-- secure-release-review-model.md
    |   |-- human-approval-policy.md
    |
    |-- fixtures/
    |   |-- vulnerable-python-app/
    |   |-- insecure-dockerfile/
    |   |-- insecure-kubernetes/
    |   |-- sample-scan-results/
    |
    |-- reports/
    |
    |-- evidence/
    |   |-- ai-assisted-secure-sdlc-summary.md
    |
    |-- .github/workflows/
    |   |-- ai-assisted-pr-review.yml
    |   |-- release-security-review.yml

## Main Commands

Show available commands:

    make help

Run AI-assisted PR security review:

    make ai-review

Run release security review:

    make release-review

Run finding triage assistant:

    make triage

Run all local reviews:

    make all

## Output Reports

Generated reports are written to:

    reports/

Important reports:

| Report | Purpose |
|---|---|
| ai-assisted-security-review.md | PR/code security review summary |
| release-security-review.md | Release readiness security decision |
| finding-triage-report.md | Vulnerability triage and prioritization summary |

## Security Philosophy

AI-assisted security should support human reviewers, not bypass them.

This project follows these principles:

- AI output is advisory
- high-risk changes require human approval
- secrets must never be exposed to AI prompts
- generated code must be scanned and reviewed
- security gates must be explainable
- release decisions should be evidence-based
- automation should not approve its own risky changes

## Interview Explanation

I created this project to demonstrate how AI-assisted engineering can support Secure SDLC and software release management.

The project reviews code, Dockerfiles, Kubernetes manifests, and sample scan outputs to generate structured security summaries.

It helps identify risky code patterns, insecure configuration, missing security controls, and release readiness gaps.

The important point is that the AI-assisted workflow does not replace human approval. It supports security decision-making by generating evidence, highlighting risk, and recommending whether a release should pass, pass with warnings, or be blocked.
