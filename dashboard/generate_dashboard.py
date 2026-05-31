from pathlib import Path
import json
import re
from datetime import datetime, UTC

REPORTS = {
    "insecure": Path("reports/ai-assisted-security-review-insecure.md"),
    "secure": Path("reports/ai-assisted-security-review-secure.md"),
    "triage": Path("reports/finding-triage-report.md"),
    "release": Path("reports/release-security-review.md"),
}

DASHBOARD = Path("dashboard/security-dashboard.html")
METRICS = Path("dashboard/secure-sdlc-metrics.prom")


def read(path):
    return path.read_text(errors="ignore") if path.exists() else ""


def count_severity(text, severity):
    return len(re.findall(rf"Severity:\s*{severity}", text, flags=re.IGNORECASE))


def get_decision(text):
    match = re.search(r"Decision:\s*(.+)", text)
    if match:
        return match.group(1).strip()
    match = re.search(r"Release decision:\s*(.+)", text)
    if match:
        return match.group(1).strip()
    return "UNKNOWN"


def generate():
    insecure = read(REPORTS["insecure"])
    secure = read(REPORTS["secure"])
    triage = read(REPORTS["triage"])
    release = read(REPORTS["release"])

    insecure_high = count_severity(insecure, "HIGH")
    insecure_medium = count_severity(insecure, "MEDIUM")
    secure_high = count_severity(secure, "HIGH")
    secure_medium = count_severity(secure, "MEDIUM")

    release_decision = get_decision(release)
    insecure_decision = get_decision(insecure)
    secure_decision = get_decision(secure)

    p1 = len(re.findall(r"Suggested priority:\s*P1", triage))
    p2 = len(re.findall(r"Suggested priority:\s*P2", triage))
    p3 = len(re.findall(r"Suggested priority:\s*P3", triage))
    p4 = len(re.findall(r"Suggested priority:\s*P4", triage))

    DASHBOARD.parent.mkdir(exist_ok=True)

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AI-Assisted Secure SDLC Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; background: #f6f8fa; color: #24292f; }}
    h1 {{ margin-bottom: 4px; }}
    .subtitle {{ color: #57606a; margin-bottom: 24px; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
    .card {{ background: white; border: 1px solid #d0d7de; border-radius: 12px; padding: 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }}
    .metric {{ font-size: 32px; font-weight: bold; margin-top: 8px; }}
    .block {{ color: #cf222e; }}
    .pass {{ color: #1a7f37; }}
    .warn {{ color: #9a6700; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; border: 1px solid #d0d7de; }}
    th, td {{ padding: 12px; border-bottom: 1px solid #d0d7de; text-align: left; }}
    th {{ background: #f0f3f6; }}
    pre {{ background: #0d1117; color: #c9d1d9; padding: 16px; border-radius: 12px; overflow: auto; }}
  </style>
</head>
<body>
  <h1>AI-Assisted Secure SDLC Dashboard</h1>
  <div class="subtitle">Generated: {datetime.now(UTC).isoformat()} UTC</div>

  <div class="grid">
    <div class="card">
      <div>Release Decision</div>
      <div class="metric {'block' if release_decision == 'BLOCK' else 'pass'}">{release_decision}</div>
    </div>
    <div class="card">
      <div>Insecure Profile</div>
      <div class="metric block">{insecure_decision}</div>
    </div>
    <div class="card">
      <div>Secure Profile</div>
      <div class="metric pass">{secure_decision}</div>
    </div>
    <div class="card">
      <div>High Findings</div>
      <div class="metric block">{insecure_high}</div>
    </div>
  </div>

  <h2>Security Review Comparison</h2>
  <table>
    <tr><th>Profile</th><th>Decision</th><th>High</th><th>Medium</th><th>Meaning</th></tr>
    <tr><td>Insecure fixture</td><td>{insecure_decision}</td><td>{insecure_high}</td><td>{insecure_medium}</td><td>Unsafe release should be stopped</td></tr>
    <tr><td>Secure fixture</td><td>{secure_decision}</td><td>{secure_high}</td><td>{secure_medium}</td><td>Clean profile should pass advisory review</td></tr>
  </table>

  <h2>Triage Priority Summary</h2>
  <table>
    <tr><th>Priority</th><th>Count</th></tr>
    <tr><td>P1</td><td>{p1}</td></tr>
    <tr><td>P2</td><td>{p2}</td></tr>
    <tr><td>P3</td><td>{p3}</td></tr>
    <tr><td>P4</td><td>{p4}</td></tr>
  </table>

  <h2>Release Review</h2>
  <pre>{release}</pre>
</body>
</html>
"""
    DASHBOARD.write_text(html)

    release_block = 1 if release_decision == "BLOCK" else 0
    release_pass = 1 if release_decision == "PASS" else 0
    release_warn = 1 if release_decision == "PASS WITH WARNINGS" else 0

    metrics = f"""# HELP secure_sdlc_findings_total AI-assisted Secure SDLC findings by profile and severity
# TYPE secure_sdlc_findings_total gauge
secure_sdlc_findings_total{{profile="insecure",severity="high"}} {insecure_high}
secure_sdlc_findings_total{{profile="insecure",severity="medium"}} {insecure_medium}
secure_sdlc_findings_total{{profile="secure",severity="high"}} {secure_high}
secure_sdlc_findings_total{{profile="secure",severity="medium"}} {secure_medium}
# HELP secure_sdlc_release_decision Release decision as one-hot gauge
# TYPE secure_sdlc_release_decision gauge
secure_sdlc_release_decision{{decision="block"}} {release_block}
secure_sdlc_release_decision{{decision="pass"}} {release_pass}
secure_sdlc_release_decision{{decision="pass_with_warnings"}} {release_warn}
# HELP secure_sdlc_triage_priority_total Finding triage count by priority
# TYPE secure_sdlc_triage_priority_total gauge
secure_sdlc_triage_priority_total{{priority="P1"}} {p1}
secure_sdlc_triage_priority_total{{priority="P2"}} {p2}
secure_sdlc_triage_priority_total{{priority="P3"}} {p3}
secure_sdlc_triage_priority_total{{priority="P4"}} {p4}
"""
    METRICS.write_text(metrics)

    print(f"Dashboard written to {DASHBOARD}")
    print(f"Metrics written to {METRICS}")


if __name__ == "__main__":
    generate()
