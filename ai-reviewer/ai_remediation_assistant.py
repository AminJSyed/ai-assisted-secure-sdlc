from pathlib import Path
import re

from ai_provider import AIProvider

REVIEW_REPORT = Path("reports/ai-assisted-security-review.md")
RISK_SCORE_REPORT = Path("reports/security-risk-score.md")
EXECUTIVE_SUMMARY = Path("reports/executive-release-summary.md")
OUTPUT = Path("reports/ai-assisted-remediation-plan.md")


REMEDIATION_LIBRARY = {
    "PY-SQL-INJECTION": {
        "summary": "SQL query is built using string concatenation.",
        "recommended_fix": "Use parameterized queries or prepared statements.",
        "example": 'cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))',
        "owner": "Application developer",
    },
    "PY-COMMAND-INJECTION": {
        "summary": "Shell command execution is using shell=True.",
        "recommended_fix": "Avoid shell=True and pass arguments as a list after validation.",
        "example": 'subprocess.check_output(["ping", "-c", "1", host])',
        "owner": "Application developer",
    },
    "SECRET-HARDCODED": {
        "summary": "A hardcoded key or secret-like value was detected.",
        "recommended_fix": "Move secrets to environment variables, CI/CD secrets, or a secret manager. Rotate exposed values.",
        "example": 'API_KEY = os.getenv("API_KEY", "")',
        "owner": "Application developer / platform owner",
    },
    "DOCKER-MISSING-USER": {
        "summary": "Container image does not define a non-root runtime user.",
        "recommended_fix": "Create a dedicated user and run the container with USER.",
        "example": "RUN useradd -u 10001 appuser\nUSER appuser",
        "owner": "Platform / DevOps engineer",
    },
    "DOCKER-MISSING-HEALTHCHECK": {
        "summary": "Docker image does not define a health check.",
        "recommended_fix": "Add a HEALTHCHECK instruction to improve runtime observability.",
        "example": 'HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen(\'http://127.0.0.1:5000/\')"',
        "owner": "Platform / DevOps engineer",
    },
    "K8S-MISSING-SECURITYCONTEXT": {
        "summary": "Kubernetes workload is missing securityContext hardening.",
        "recommended_fix": "Set runAsNonRoot, drop capabilities, disable privilege escalation, and use RuntimeDefault seccomp.",
        "example": "securityContext:\n  allowPrivilegeEscalation: false\n  capabilities:\n    drop:\n      - ALL",
        "owner": "Platform / Kubernetes engineer",
    },
    "K8S-MISSING-RESOURCE-LIMITS": {
        "summary": "Kubernetes workload is missing CPU or memory requests and limits.",
        "recommended_fix": "Add resource requests and limits for predictable scheduling and resource governance.",
        "example": 'resources:\n  requests:\n    cpu: "100m"\n    memory: "128Mi"\n  limits:\n    cpu: "500m"\n    memory: "256Mi"',
        "owner": "Platform / Kubernetes engineer",
    },
}


def read(path: Path) -> str:
    return path.read_text(errors="ignore") if path.exists() else ""


def parse_rule_ids(markdown: str):
    return re.findall(r"^###\s+([A-Z0-9-]+)", markdown, flags=re.MULTILINE)


def main():
    OUTPUT.parent.mkdir(exist_ok=True)

    review = read(REVIEW_REPORT)
    risk_score = read(RISK_SCORE_REPORT)
    executive = read(EXECUTIVE_SUMMARY)

    rule_ids = parse_rule_ids(review)

    prompt = (
        "Create a concise secure remediation plan for these AI-assisted Secure SDLC findings.\n\n"
        "Security review:\n"
        f"{review}\n\n"
        "Risk score:\n"
        f"{risk_score}\n\n"
        "Executive summary:\n"
        f"{executive}\n"
    )

    provider = AIProvider()
    provider_summary = provider.generate(prompt)

    lines = []
    lines.append("# AI-Assisted Remediation Plan")
    lines.append("")
    lines.append("## Provider Summary")
    lines.append("")
    lines.append(provider_summary)
    lines.append("")
    lines.append("## Remediation Plan")
    lines.append("")

    if not rule_ids:
        lines.append("No findings detected. No remediation plan required.")
    else:
        for index, rule_id in enumerate(rule_ids, start=1):
            item = REMEDIATION_LIBRARY.get(rule_id, {})
            lines.append(f"### {index}. {rule_id}")
            lines.append("")
            lines.append(f"- Summary: {item.get('summary', 'Security issue detected.')}")
            lines.append(f"- Recommended fix: {item.get('recommended_fix', 'Review and remediate according to secure coding standards.')}")
            lines.append(f"- Suggested owner: {item.get('owner', 'Security reviewer / engineering owner')}")
            lines.append("- Example remediation:")
            lines.append("")
            lines.append("    " + item.get("example", "Review the finding and apply a secure fix.").replace("\n", "\n    "))
            lines.append("")

    lines.append("## Human Review Requirement")
    lines.append("")
    lines.append("This remediation plan is AI-assisted decision support. A human reviewer must validate the fix before merge or release.")

    OUTPUT.write_text("\n".join(lines))
    print(OUTPUT.read_text())


if __name__ == "__main__":
    main()
