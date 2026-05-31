# Human Approval Policy

## Purpose

This policy defines when human approval is required in AI-assisted security workflows.

## Always Require Human Approval For

- production deployments
- disabling security controls
- changing CI/CD permissions
- modifying authentication logic
- modifying authorization logic
- changing secrets handling
- changing Kubernetes RBAC
- accepting critical or high vulnerabilities
- merging code with known exploitability
- release promotion to production

## Why This Matters

AI-assisted workflows can speed up review, but they should not become unchecked automation.

Human approval keeps accountability, context, and business risk decisions in the process.
