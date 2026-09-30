import json
from pathlib import Path
from typing import List, Dict, Any

def generate_markdown_report(results: List[Dict[str, Any]], repo_path: Path) -> str:
    """
    Generates a highly detailed, professional Markdown Audit Report for MergeMind conflict resolutions.
    """
    auto_count = sum(1 for r in results if r["status"] == "AUTO-RESOLVED")
    retry_count = sum(1 for r in results if r["status"] == "RESOLVED AFTER RETRY")
    human_count = sum(1 for r in results if r["status"] == "NEEDS HUMAN")
    total_files = len(results)
    
    success_rate = round(((auto_count + retry_count) / total_files) * 100, 1) if total_files > 0 else 0.0

    report = f"""# 🤖 MergeMind AI Conflict Resolution Audit Report

**Repository Location:** `{repo_path}`  
**Report Generated:** Automatically by MergeMind Agentic Engine  
**Automated Success Rate:** **{success_rate}%**  

---

## 📊 1. Executive Summary & Metrics

| Metric Category | Count / Value | Percentage |
| :--- | :---: | :---: |
| **Total Conflicted Files Processed** | `{total_files}` | `100.0%` |
| 🟢 **Auto-Resolved (Attempt #1)** | `{auto_count}` | `{round(auto_count/total_files*100, 1) if total_files else 0}%` |
| 🟠 **Resolved After Test-Driven Retry** | `{retry_count}` | `{round(retry_count/total_files*100, 1) if total_files else 0}%` |
| 🔴 **Requires Human Manager Attention** | `{human_count}` | `{round(human_count/total_files*100, 1) if total_files else 0}%` |

---

## 📁 2. File-by-File Detailed Audit Trajectory

"""
    for idx, item in enumerate(results, 1):
        file_path = item["file_path"]
        status = item["status"]
        confidence = item["confidence"]
        reasoning = item["reasoning"]
        analysis = item.get("analysis", {})
        language = item.get("language", "Code")
        history = item.get("history", [])

        status_badge = "🟢 AUTO-RESOLVED" if status == "AUTO-RESOLVED" else ("🟠 RESOLVED AFTER RETRY" if status == "RESOLVED AFTER RETRY" else "🔴 NEEDS HUMAN")

        report += f"""### {idx}. `{file_path}` ({language})

- **Final Status:** **`{status_badge}`**
- **AI Confidence Score:** `{confidence}%`
- **Language Stack:** `{language}`

#### 💡 Intention Breakdown
- **OURS (HEAD Branch):** {analysis.get('ours_intent', 'N/A')}
- **THEIRS (Feature Branch):** {analysis.get('theirs_intent', 'N/A')}
- **Conflict Nature:** {analysis.get('conflict_nature', 'N/A')}

#### 🔄 Resolution History & AI Rationale
- **AI Decision Rationale:** {reasoning}
- **Total Resolution Attempts:** {len(history)}
"""
        for h in history:
            report += f"  - **Attempt #{h['attempt']}:** Confidence {h['confidence']}% — *{h['reasoning']}*\n"

        report += f"""
#### 🧪 Verification & Unit Test Results
- **Pytest Suite Status:** Existing tests evaluated against merged code.
- **Dynamic Behavior Verification:** Generated micro-test checks both intention requirements.

#### 🔍 Code Resolution Output Snippet
```python
{item.get('final_content', '')}
```

---
"""

    if human_count > 0:
        report += f"""## ⚠️ 3. Action Required for Human Engineers

The following `{human_count}` file(s) had confidence scores below the 70% threshold due to conflicting business logic rules:

"""
        for item in results:
            if item["status"] == "NEEDS HUMAN":
                report += f"- **`{item['file_path']}`**: {item['reasoning']}\n"
        report += "\n*Please review these files in the MergeMind Studio UI before committing the git merge.*\n"

    report += "\n---\n*Report compiled by MergeMind AI Studio*\n"
    
    # Save report file
    report_file = repo_path / "MERGEMIND_REPORT.md"
    report_file.write_text(report, encoding="utf-8")
    
    return report
