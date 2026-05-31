# Dashboarding and Observability

## Purpose

This project includes dashboarding to make AI-assisted Secure SDLC decisions visible.

The goal is to show security review results, release decisions, finding severity, and triage priorities in a clear visual format.

## Dashboard Types

| Dashboard | Purpose |
|---|---|
| HTML dashboard | Simple local dashboard for screenshots and evidence |
| Prometheus metrics | Machine-readable Secure SDLC metrics |
| Grafana dashboard | Visual monitoring dashboard for release/security posture |

## Metrics Exposed

| Metric | Meaning |
|---|---|
| secure_sdlc_findings_total | Findings by profile and severity |
| secure_sdlc_release_decision | Release decision as one-hot gauge |
| secure_sdlc_triage_priority_total | Finding count by priority |

## Local Commands

Generate reports and HTML dashboard:

    make dashboard

Start metrics server:

    make metrics

Start Prometheus and Grafana:

    make monitoring

Open Grafana:

    http://localhost:3002

Login:

    admin / admin123

Open Prometheus:

    http://localhost:9091

Open metrics endpoint:

    http://localhost:9200/metrics

## Interview Explanation

I added dashboarding and observability to make the AI-assisted Secure SDLC workflow visible.

The project generates markdown evidence, an HTML dashboard, Prometheus metrics, and a Grafana dashboard.

This helps security teams, release managers, and engineering leaders quickly understand whether a release is blocked, what findings exist, which priorities need attention, and whether secure fixtures pass the review.
