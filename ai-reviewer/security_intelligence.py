from pathlib import Path
import json
import re

REVIEW_REPORT = Path("reports/ai-assisted-security-review.md")
TRIAGE_REPORT = Path("reports/finding-triage-report.md")
RELEASE_REPORT = Path("reports/release-security-review.md")

SARIF_OUTPUT = Path("reports/ai-assisted-findings.sarif")
EXECUTIVE_SUMMARY = Path("reports/executive-release-summary.md")
RISK_SCORE_REPORT = Path("reports/security-risk-score.md")

RULE_METADATA = {
    "PY-SQL-INJECTION": {
        "cwe": "CWE-89",
        "owasp": "A03:2021 Injection",
        "remediation": "Use parameterized queries or prepared statements. Never build SQL queries by concatenating user input.",
        "risk_weight": 30,
    },
    "PY-COMMAND-INJECTION": {
        "cwe": "CWE-78",
        "owasp": "A03:2021 Injection",
        "remediation": "Avoid shell=True. Pass command arguments as a list and validate user-controlled input.",
        "risk_weight": 30,
    },
    "SECRET-HARDCODED": {
        "cwe": "CWE-798",
        "owasp": "A02:2021 Cryptographic Failures",
        "remediation": "Move secrets to environment variables, a secret manager, or CI/CD protected secrets. Rotate exposed credentials.",
        "risk_weight": 15,
    },
    "DOCKER-MISSING-USER": {
        "cwe": "CWE-250",
        "owasp": "Container Hardening",
        "remediation": "Create and use a non-root user in the Docker image.",
        "risk_weight": 20,
    },
    "DOCKER-MISSING-HEALTHCHECK": {
        "cwe": "CWE-703",
        "owasp": "Operational Resilience",
        "remediation": "Add a Docker HEALTHCHECK instruction to detect unhealthy containers.",
        "risk_weight": 10,
    },
    "K8S-MISSING-SECURITYCONTEXT": {
        "cwe": "CWE-250",
        "owasp": "Kubernetes Hardening",
        "remediation": "Set runAsNonRoot, allowPrivilegeEscalation false, drop Linux capabilities, and use RuntimeDefault seccomp.",
        "risk_weight": 15,
    },
    "K8S-MISSING-RESOURCE-LIMITS": {
        "cwe": "CWE-770",
        "owasp": "Kubernetes Resource Governance",
        "remediation": "Add CPU and memory requests and limits to reduce noisy-neighbor and resource exhaustion risk.",
        "risk_weight": 10,
    },
}


def read_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(errors="ignore")


def parse_review_findings(markdown: str):
    findings = []
    blocks = re.split(r"\n### ", markdown)

    for block in blocks[1:]:
        lines = block.splitlines()
        if not lines:
            continue

        rule_id = lines[0].strip()
        severity = "UNKNOWN"
        file_path = "unknown"
        observation = ""
        recommendation = ""

        for line in lines:
            if line.startswith("- Severity:"):
                severity = line.replace("- Severity:", "").strip()
            elif line.startswith("- File:"):
                file_path = line.replace("- File:", "").strip()
            elif line.startswith("- Observation:"):
                observation = line.replace("- Observation:", "").strip()
            elif line.startswith("- Recommendation:"):
                recommendation = line.replace("- Recommendation:", "").strip()

        metadata = RULE_METADATA.get(rule_id, {})
        findings.append(
            {
                "rule_id": rule_id,
                "severity": severity.upper(),
                "file": file_path,
                "observation": observation,
                "recommendation": recommendation,
                "cwe": metadata.get("cwe", "N/A"),
                "owasp": metadata.get("owasp", "N/A"),
                "ai_remediation": metadata.get("remediation", recommendation),
                "risk_weight": metadata.get("risk_weight", 5),
            }
        )

    return findings


def sarif_level(severity: str) -> str:
    severity = severity.upper()
    if severity in ["CRITICAL", "HIGH"]:
        return "error"
    if severity == "MEDIUM":
        return "warning"
    return "note"


def generate_sarif(findings):
    rules = []
    results = []

    seen_rules = set()

    for finding in findings:
        rule_id = finding["rule_id"]

        if rule_id not in seen_rules:
            seen_rules.add(rule_id)
            rules.append(
                {
                    "id": rule_id,
                    "name": rule_id,
                    "shortDescription": {
                        "text": finding["observation"] or rule_id
                    },
                    "fullDescription": {
                        "text": finding["ai_remediation"]
                    },
                    "help": {
                        "text": f"CWE: {finding['cwe']}. OWASP/Control: {finding['owasp']}. Remediation: {finding['ai_remediation']}"
                    },
                    "properties": {
                        "tags": [
                            "ai-assisted-secure-sdlc",
                            finding["cwe"],
                            finding["owasp"],
                        ]
                    },
                }
            )

        results.append(
            {
                "ruleId": rule_id,
                "level": sarif_level(finding["severity"]),
                "message": {
                    "text": f"{finding['observation']} Suggested remediation: {finding['ai_remediation']}"
                },
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": finding["file"]
                            },
                            "region": {
                                "startLine": 1
                            },
                        }
                    }
                ],
                "properties": {
                    "severity": finding["severity"],
                    "cwe": finding["cwe"],
                    "owasp": finding["owasp"],
                    "ai_remediation": finding["ai_remediation"],
                },
            }
        )

    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "AI-Assisted Secure SDLC Reviewer",
                        "informationUri": "https://github.com/AminJSyed/ai-assisted-secure-sdlc",
                        "rules": rules,
                    }
                },
                "results": results,
            }
        ],
    }

    SARIF_OUTPUT.parent.mkdir(exist_ok=True)
    SARIF_OUTPUT.write_text(json.dumps(sarif, indent=2))


def calculate_risk_score(findings):
    score = 0

    for finding in findings:
        score += finding.get("risk_weight", 5)

    score = min(score, 100)

    if score >= 70:
        rating = "HIGH"
        decision = "BLOCK"
    elif score >= 30:
        rating = "MEDIUM"
        decision = "REVIEW REQUIRED"
    else:
        rating = "LOW"
        decision = "PASS"

    return score, rating, decision


def generate_risk_score_report(findings, score, rating, decision):
    lines = []
    lines.append("# Security Risk Score")
    lines.append("")
    lines.append(f"Risk score: {score}/100")
    lines.append(f"Risk rating: {rating}")
    lines.append(f"Recommended decision: {decision}")
    lines.append("")
    lines.append("## Scoring Inputs")
    lines.append("")

    if not findings:
        lines.append("No findings detected.")
    else:
        for finding in findings:
            lines.append(f"- {finding['rule_id']} | {finding['severity']} | Weight: {finding['risk_weight']} | File: {finding['file']}")

    lines.append("")
    lines.append("## Note")
    lines.append("")
    lines.append("This score is advisory and should be reviewed by a human security owner before production release.")

    RISK_SCORE_REPORT.write_text("\n".join(lines))


def generate_executive_summary(findings, score, rating, decision):
    high = sum(1 for f in findings if f["severity"] == "HIGH")
    medium = sum(1 for f in findings if f["severity"] == "MEDIUM")
    low = sum(1 for f in findings if f["severity"] == "LOW")

    lines = []
    lines.append("# Executive Release Security Summary")
    lines.append("")
    lines.append(f"Release decision: {decision}")
    lines.append(f"Security risk score: {score}/100")
    lines.append(f"Risk rating: {rating}")
    lines.append("")
    lines.append("## Finding Summary")
    lines.append("")
    lines.append(f"- High findings: {high}")
    lines.append(f"- Medium findings: {medium}")
    lines.append(f"- Low findings: {low}")
    lines.append("")
    lines.append("## Key Risk Areas")
    lines.append("")

    if not findings:
        lines.append("No risky patterns detected in the reviewed files.")
    else:
        for finding in findings:
            lines.append(f"- {finding['severity']}: {finding['observation']} ({finding['file']})")

    lines.append("")
    lines.append("## Recommended Actions")
    lines.append("")

    if not findings:
        lines.append("- Continue release review and keep required security evidence attached.")
    else:
        for finding in findings:
            lines.append(f"- {finding['rule_id']}: {finding['ai_remediation']}")

    lines.append("")
    lines.append("## Human Approval")
    lines.append("")
    lines.append("This executive summary is generated as AI-assisted decision support. Production release approval must remain with an authorized human reviewer.")

    EXECUTIVE_SUMMARY.write_text("\n".join(lines))


def main():
    review = read_file(REVIEW_REPORT)
    findings = parse_review_findings(review)

    score, rating, decision = calculate_risk_score(findings)

    generate_sarif(findings)
    generate_risk_score_report(findings, score, rating, decision)
    generate_executive_summary(findings, score, rating, decision)

    print(EXECUTIVE_SUMMARY.read_text())
    print("")
    print(RISK_SCORE_REPORT.read_text())
    print("")
    print(f"SARIF written to {SARIF_OUTPUT}")


if __name__ == "__main__":
    main()
