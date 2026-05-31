# AI Provider Integration

## Purpose

This document explains how AI-assisted behavior is handled in this project.

The project is safe by default and does not require a real AI provider or API key.

## Provider Modes

| Mode | Purpose |
|---|---|
| rule_based | Default deterministic mode. Safe for CI/CD and does not call external services |
| mock | Simulates an LLM-style summary without external calls |
| external | Optional mode for integrating with an approved external AI gateway |

## Default Mode

The default mode is:

    AI_PROVIDER=rule_based

This keeps the project repeatable and safe for GitHub Actions.

## Mock Mode

Mock mode can be used to demonstrate LLM-style behavior locally:

    AI_PROVIDER=mock make ai-remediation

## External Mode

External mode is optional.

It requires:

    AI_PROVIDER=external
    AI_API_URL=<approved-ai-gateway-url>
    AI_API_KEY=<stored-in-secret-manager-or-github-secret>

No real API key should be committed to the repository.

## Security Requirements

External AI integration must follow these rules:

- do not send real secrets
- do not send production credentials
- do not send private customer data
- use approved gateways only
- store API keys in GitHub Secrets or a secret manager
- keep human approval for high-risk decisions
- log AI-assisted decisions as advisory evidence

## Why This Matters

This approach allows the project to demonstrate AI-assisted security engineering while keeping the default workflow safe, deterministic, and CI/CD friendly.
