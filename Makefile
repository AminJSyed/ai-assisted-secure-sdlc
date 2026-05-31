.PHONY: help ai-review triage release-review all clean ai-review-secure ai-review-insecure dashboard metrics monitoring monitoring-down demo-pr

help:
	@echo "AI-Assisted Secure SDLC Commands"
	@echo ""
	@echo "make ai-review       - Run AI-assisted code and config security review"
	@echo "make triage          - Run finding triage assistant"
	@echo "make release-review  - Run release security review"
	@echo "make security-intelligence - Generate SARIF, risk score, and executive summary"
	@echo "make ai-remediation - Generate AI-assisted remediation plan"
	@echo "make dashboard       - Generate HTML dashboard and Prometheus metrics"
	@echo "make monitoring      - Start Prometheus and Grafana dashboard"
	@echo "make monitoring-down - Stop Prometheus and Grafana dashboard"
	@echo "make demo-pr        - Create demo insecure PR branch"
	@echo "make all             - Run all reviews"
	@echo "make clean           - Remove generated reports"

ai-review:
	python3 ai-reviewer/review_changed_files.py

triage:
	python3 ai-reviewer/finding_triage_assistant.py

release-review:
	python3 ai-reviewer/release_security_review.py

all: ai-review triage release-review security-intelligence ai-remediation

clean:
	rm -rf reports/*

ai-review-secure:
	python3 ai-reviewer/review_changed_files.py --profile secure --output reports/ai-assisted-security-review-secure.md

ai-review-insecure:
	python3 ai-reviewer/review_changed_files.py --profile insecure --output reports/ai-assisted-security-review-insecure.md

dashboard: ai-review-insecure ai-review-secure triage release-review
	python3 dashboard/generate_dashboard.py

metrics: dashboard
	python3 dashboard/metrics_server.py

monitoring: dashboard
	docker compose -f docker-compose.monitoring.yml up -d --build

monitoring-down:
	docker compose -f docker-compose.monitoring.yml down


demo-pr:
	./scripts/create-demo-pr-change.sh


security-intelligence:
	python3 ai-reviewer/security_intelligence.py


ai-remediation:
	python3 ai-reviewer/ai_remediation_assistant.py
