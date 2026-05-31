import json
from pathlib import Path

INPUT = Path("fixtures/sample-scan-results/sample-findings.json")
OUTPUT = Path("reports/finding-triage-report.md")


def priority(finding):
    severity = finding.get("severity", "").lower()
    exposed = finding.get("runtime_exposed", False)
    fix = finding.get("fix_available", False)

    if severity in ["critical", "high"] and exposed:
        return "P1"
    if severity in ["critical", "high"]:
        return "P2"
    if severity == "medium" and exposed and fix:
        return "P2"
    if severity == "medium":
        return "P3"
    return "P4"


def main():
    findings = json.loads(INPUT.read_text())
    OUTPUT.parent.mkdir(exist_ok=True)

    lines = ["# AI-Assisted Finding Triage", ""]

    for finding in findings:
        p = priority(finding)
        lines.append(f"## {finding['id']} - {finding['title']}")
        lines.append("")
        lines.append(f"- Tool: {finding['tool']}")
        lines.append(f"- Severity: {finding['severity']}")
        lines.append(f"- File: {finding['file']}")
        lines.append(f"- Runtime exposed: {finding['runtime_exposed']}")
        lines.append(f"- Fix available: {finding['fix_available']}")
        lines.append(f"- Suggested priority: {p}")
        lines.append("")

    lines.append("## Triage Note")
    lines.append("")
    lines.append("This triage is advisory and should be validated by a human security reviewer.")

    OUTPUT.write_text("\n".join(lines))
    print(OUTPUT.read_text())


if __name__ == "__main__":
    main()
