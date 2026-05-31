from pathlib import Path
import argparse
import re

REPORT_PATH = Path("reports/ai-assisted-security-review.md")

TARGET_PROFILES = {
    "insecure": [
        Path("fixtures/vulnerable-python-app/app.py"),
        Path("fixtures/insecure-dockerfile/Dockerfile"),
        Path("fixtures/insecure-kubernetes/deployment.yaml"),
    ],
    "secure": [
        Path("fixtures/secure-python-app/app.py"),
        Path("fixtures/secure-dockerfile/Dockerfile"),
        Path("fixtures/secure-kubernetes/deployment.yaml"),
    ],
}

RULES = [
    {
        "id": "PY-SQL-INJECTION",
        "severity": "HIGH",
        "pattern": r"SELECT .* \+",
        "message": "Possible SQL injection through string concatenation.",
        "recommendation": "Use parameterized queries."
    },
    {
        "id": "PY-COMMAND-INJECTION",
        "severity": "HIGH",
        "pattern": r"shell=True",
        "message": "Possible command injection through shell=True.",
        "recommendation": "Avoid shell=True and pass arguments as a list."
    },
    {
        "id": "SECRET-HARDCODED",
        "severity": "MEDIUM",
        "pattern": r"API_KEY\s*=\s*[\"']",
        "message": "Possible hardcoded API key.",
        "recommendation": "Use environment variables or a secret manager."
    },
    {
        "id": "DOCKER-MISSING-USER",
        "severity": "HIGH",
        "pattern": r"^FROM ",
        "message": "Dockerfile should define a non-root USER.",
        "recommendation": "Create and use a non-root user in the image."
    },
    {
        "id": "DOCKER-MISSING-HEALTHCHECK",
        "severity": "MEDIUM",
        "pattern": r"^FROM ",
        "message": "Dockerfile should define a HEALTHCHECK.",
        "recommendation": "Add a HEALTHCHECK instruction."
    },
    {
        "id": "K8S-MISSING-SECURITYCONTEXT",
        "severity": "MEDIUM",
        "pattern": r"containers:",
        "message": "Kubernetes workload should include securityContext.",
        "recommendation": "Set runAsNonRoot, drop capabilities, disable privilege escalation, and use seccomp."
    },
    {
        "id": "K8S-MISSING-RESOURCE-LIMITS",
        "severity": "MEDIUM",
        "pattern": r"containers:",
        "message": "Kubernetes workload should include resource requests and limits.",
        "recommendation": "Add CPU and memory requests and limits."
    }
]


def scan_file(path: Path):
    findings = []
    if not path.exists():
        return findings

    content = path.read_text(errors="ignore")

    for rule in RULES:
        if re.search(rule["pattern"], content, re.MULTILINE):
            if rule["id"] == "DOCKER-MISSING-USER" and "USER " in content:
                continue
            if rule["id"] == "DOCKER-MISSING-HEALTHCHECK" and "HEALTHCHECK" in content:
                continue
            if rule["id"] == "K8S-MISSING-SECURITYCONTEXT" and "securityContext:" in content:
                continue
            if rule["id"] == "K8S-MISSING-RESOURCE-LIMITS" and "resources:" in content and "limits:" in content and "requests:" in content:
                continue

            findings.append({
                "file": str(path),
                **rule
            })

    return findings


def decision(findings):
    if any(f["severity"] == "HIGH" for f in findings):
        return "BLOCK RECOMMENDED"
    if findings:
        return "REVIEW REQUIRED"
    return "PASS"


def generate_report(profile: str, output: Path):
    targets = TARGET_PROFILES[profile]
    output.parent.mkdir(exist_ok=True)

    all_findings = []
    for target in targets:
        all_findings.extend(scan_file(target))

    result = decision(all_findings)

    lines = []
    lines.append("# AI-Assisted Security Review")
    lines.append("")
    lines.append(f"Profile: {profile}")
    lines.append("")
    lines.append(f"Decision: {result}")
    lines.append("")
    lines.append("## Reviewed Files")
    lines.append("")
    for target in targets:
        lines.append(f"- {target}")
    lines.append("")
    lines.append("## Findings")
    lines.append("")

    if not all_findings:
        lines.append("No risky patterns detected.")
    else:
        for finding in all_findings:
            lines.append(f"### {finding['id']}")
            lines.append("")
            lines.append(f"- Severity: {finding['severity']}")
            lines.append(f"- File: {finding['file']}")
            lines.append(f"- Observation: {finding['message']}")
            lines.append(f"- Recommendation: {finding['recommendation']}")
            lines.append("")

    lines.append("## Human Review Note")
    lines.append("")
    lines.append("This AI-assisted review is advisory. High-risk findings require human review before merge.")

    output.write_text("\n".join(lines))
    return result, all_findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=["insecure", "secure"], default="insecure")
    parser.add_argument("--output", default=str(REPORT_PATH))
    parser.add_argument("--paths", nargs="*", help="Optional custom file paths to scan instead of profile fixtures")
    args = parser.parse_args()

    if args.paths:
        custom_targets = [Path(p) for p in args.paths]
        output = Path(args.output)
        output.parent.mkdir(exist_ok=True)

        all_findings = []
        for target in custom_targets:
            all_findings.extend(scan_file(target))

        result = decision(all_findings)

        lines = []
        lines.append("# AI-Assisted Security Review")
        lines.append("")
        lines.append("Profile: custom")
        lines.append("")
        lines.append(f"Decision: {result}")
        lines.append("")
        lines.append("## Reviewed Files")
        lines.append("")
        for target in custom_targets:
            lines.append(f"- {target}")
        lines.append("")
        lines.append("## Findings")
        lines.append("")

        if not all_findings:
            lines.append("No risky patterns detected.")
        else:
            for finding in all_findings:
                lines.append(f"### {finding['id']}")
                lines.append("")
                lines.append(f"- Severity: {finding['severity']}")
                lines.append(f"- File: {finding['file']}")
                lines.append(f"- Observation: {finding['message']}")
                lines.append(f"- Recommendation: {finding['recommendation']}")
                lines.append("")

        lines.append("## Human Review Note")
        lines.append("")
        lines.append("This AI-assisted review is advisory. High-risk findings require human review before merge.")

        output.write_text("\n".join(lines))
        print(output.read_text())
    else:
        result, findings = generate_report(args.profile, Path(args.output))
        print(Path(args.output).read_text())


if __name__ == "__main__":
    main()
