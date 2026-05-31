from pathlib import Path

OUTPUT = Path("reports/release-security-review.md")

REQUIRED_EVIDENCE = {
    "AI-assisted security review": Path("reports/ai-assisted-security-review.md"),
    "Finding triage report": Path("reports/finding-triage-report.md"),
    "Sample scan results": Path("fixtures/sample-scan-results/sample-findings.json"),
}


def main():
    OUTPUT.parent.mkdir(exist_ok=True)

    missing = []
    present = []

    for name, path in REQUIRED_EVIDENCE.items():
        if path.exists():
            present.append((name, path))
        else:
            missing.append((name, path))

    decision = "PASS" if not missing else "PASS WITH WARNINGS"

    review_report = Path("reports/ai-assisted-security-review.md")
    if review_report.exists() and "BLOCK RECOMMENDED" in review_report.read_text():
        decision = "BLOCK"

    lines = ["# Release Security Review", ""]
    lines.append(f"Release decision: {decision}")
    lines.append("")
    lines.append("## Evidence Present")
    lines.append("")
    for name, path in present:
        lines.append(f"- {name}: {path}")

    lines.append("")
    lines.append("## Evidence Missing")
    lines.append("")
    if not missing:
        lines.append("No required evidence missing.")
    else:
        for name, path in missing:
            lines.append(f"- {name}: {path}")

    lines.append("")
    lines.append("## Human Approval Note")
    lines.append("")
    lines.append("Production release decisions require human approval. This report is advisory.")

    OUTPUT.write_text("\n".join(lines))
    print(OUTPUT.read_text())


if __name__ == "__main__":
    main()
