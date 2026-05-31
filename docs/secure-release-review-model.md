# Secure Release Review Model

## Purpose

This document defines how release readiness is reviewed.

## Release Evidence Checklist

Before release, the following evidence should exist:

- SAST result
- secrets scan result
- dependency scan result
- container scan result
- SBOM
- IaC or Kubernetes config scan
- DAST result where applicable
- release notes
- approval record

## Release Decision

| Decision | Criteria |
|---|---|
| PASS | Required checks present and no blocking risks |
| PASS WITH WARNINGS | Non-blocking findings exist and are documented |
| BLOCK | Critical or high-risk issue without acceptance or mitigation |

## Human Approval

Release approval should not be fully automated for high-risk changes.

AI-assisted review can recommend a decision, but human owners must approve production releases.
