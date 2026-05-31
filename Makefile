.PHONY: help ai-review triage release-review all clean

help:
	@echo "AI-Assisted Secure SDLC Commands"
	@echo ""
	@echo "make ai-review       - Run AI-assisted code and config security review"
	@echo "make triage          - Run finding triage assistant"
	@echo "make release-review  - Run release security review"
	@echo "make all             - Run all reviews"
	@echo "make clean           - Remove generated reports"

ai-review:
	python3 ai-reviewer/review_changed_files.py

triage:
	python3 ai-reviewer/finding_triage_assistant.py

release-review:
	python3 ai-reviewer/release_security_review.py

all: ai-review triage release-review

clean:
	rm -rf reports/*
