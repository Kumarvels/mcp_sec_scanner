import markdown
from datetime import datetime

SEVERITY_COLORS = {
    "Critical": "#ff4d4f",
    "High": "#faad14",
    "Medium": "#1890ff",
    "Low": "#52c41a",
    "Info": "#bfbfbf"
}

REMEDIATION_GUIDE = {
    "Hardcoded Credentials": "Remove hardcoded secrets and use environment variables or secret managers.",
    "Insecure Function": "Replace with secure alternatives and validate inputs.",
    "Outdated Dependency": "Update to the latest secure version.",
    "Weak Encryption": "Use strong, industry-standard encryption algorithms.",
    "Backdoor": "Remove unauthorized access points and review commit history.",
    "Other": "Review the code and apply best security practices."
}

def generate_markdown_report(repo_name, findings, score):
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"# Security Report for `{repo_name}`\n"
    md += f"**Generated:** {date_str}\n\n"
    md += f"## Overall Security Score: **{score}/100**\n\n"
    if not findings:
        md += "✅ No issues found. Good job!\n"
        return md

    md += "| Severity | Issue | File | Line | Recommendation |\n"
    md += "|---|---|---|---|---|\n"
    for f in findings:
        sev = f.get("severity", "Info")
        issue = f.get("issue", "Unknown")
        file = f.get("file", "N/A")
        line = f.get("line", "-")
        rec = REMEDIATION_GUIDE.get(issue, REMEDIATION_GUIDE["Other"])
        md += f"| **{sev}** | {issue} | `{file}` | {line} | {rec} |\n"
    return md

def generate_html_report(repo_name, findings, score):
    md = generate_markdown_report(repo_name, findings, score)
    html = markdown.markdown(md, extensions=['tables'])
    style = f"""
    <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 2em; background: #f9f9f9; }}
    h1 {{ color: #222; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f0f0f0; }}
    tr:nth-child(even) {{ background: #f7f7f7; }}
    .score {{ font-size: 1.5em; font-weight: bold; }}
    </style>
    """
    for sev, color in SEVERITY_COLORS.items():
        html = html.replace(f"<td><strong>{sev}</strong></td>", f"<td style='color:{color};font-weight:bold'>{sev}</td>")
    return style + html
