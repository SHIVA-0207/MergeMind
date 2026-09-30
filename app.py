import json
import os
import difflib
import subprocess
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

from mergemind.agent import process_repository
from create_demo_repo import setup_demo_repository

load_dotenv()

def finalize_git_merge(repo_path: str):
    """Finalizes the git merge commit in the target repository."""
    path = Path(repo_path).resolve()
    try:
        subprocess.run(["git", "add", "."], cwd=path, check=True)
        res = subprocess.run(
            ["git", "commit", "-m", "Merge conflict resolution finalized via MergeMind AI"],
            cwd=path,
            capture_output=True,
            text=True
        )
        return True, res.stdout
    except Exception as e:
        return False, f"Git commit failed: {e}"

st.set_page_config(
    page_title="MergeMind Studio 3.0 — AI Git Conflict Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise & Futuristic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }

    .stApp {
        background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #3B82F6 100%);
        border-radius: 16px;
        padding: 28px 32px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 6px;
        background: linear-gradient(90deg, #FFFFFF 0%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        font-weight: 400;
    }

    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700;
        color: #64748B;
    }

    .metric-val {
        font-size: 2rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 6px;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        font-size: 0.8rem;
        font-weight: 700;
        border-radius: 20px;
        letter-spacing: 0.03em;
    }
    .badge-auto { background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; }
    .badge-retry { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .badge-human { background: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }

    /* Intent Comparison Cards */
    .intent-card {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 16px 20px;
        border: 1px solid #E2E8F0;
        margin-bottom: 12px;
    }
    .intent-ours { border-left: 4px solid #3B82F6; }
    .intent-theirs { border-left: 4px solid #8B5CF6; }

    .intent-header {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .code-font {
        font-family: 'Fira Code', monospace !important;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.92rem;
        padding: 10px 22px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-title">MergeMind Studio 3.0</div>
    <div class="hero-subtitle">Autonomous AI Git Conflict Resolution Engine & Test Verification Studio</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Setup
with st.sidebar:
    st.markdown("### ⚙️ Workspace Configuration")
    repo_path_input = st.text_input("Repository Path", value="./demo_repo")
    
    api_key_env = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input("Gemini API Key", value=api_key_env, type="password", help="Reads key from environment or input")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    st.markdown("---")
    st.markdown("### 🛠️ Interactive Sandbox")
    if st.button("🔄 Reset Demo Repository", use_container_width=True):
        with st.spinner("Generating sandbox git repository..."):
            setup_demo_repository()
            if "agent_results" in st.session_state:
                del st.session_state["agent_results"]
            st.success("Sandbox repository reset at `./demo_repo`!")

    st.markdown("---")
    run_agent_btn = st.button("🚀 Analyze & Resolve Conflicts", type="primary", use_container_width=True)

repo_path = Path(repo_path_input).resolve()

# Execution Handler
if run_agent_btn:
    if not repo_path.exists():
        st.error(f"Target repository directory not found: `{repo_path}`")
    else:
        with st.spinner("MergeMind Agent is analyzing intentions and executing test suite..."):
            try:
                results = process_repository(str(repo_path))
                st.session_state["agent_results"] = results
                st.toast("Conflict resolution finished!", icon="✨")
            except Exception as e:
                st.error(f"Resolution process error: {e}")

# Interactive Workflow Diagram Tab
with st.expander("📌 View Agent Architecture & Workflow Diagram", expanded=False):
    st.markdown("#### Autonomous 5-Step Agent Loop")
    st.markdown("""
    ```mermaid
    flowchart LR
        A["1. Git Conflict Detected"] --> B["2. ANALYZE Intent (Gemini LLM)"]
        B --> C["3. PLAN & ACT (Propose Merged Code)"]
        C --> D{"4. VERIFY (pytest & Dynamic Test)"}
        D -- "Pass" --> E["🟢 AUTO-RESOLVED / RESOLVED AFTER RETRY"]
        D -- "Fail" --> F{"Retry Count < 3?"}
        F -- "Yes" --> G["4b. RE-PLAN with Error Logs"] --> C
        F -- "No" --> H["🔴 ESCALATE (NEEDS HUMAN)"]
        C -- "Confidence < 70%" --> H
    ```
    """)

# Dashboard View
if "agent_results" in st.session_state and st.session_state["agent_results"]:
    results = st.session_state["agent_results"]

    st.markdown("### 📊 Resolution Analytics Overview")
    
    auto_count = sum(1 for r in results if r["status"] == "AUTO-RESOLVED")
    retry_count = sum(1 for r in results if r["status"] == "RESOLVED AFTER RETRY")
    human_count = sum(1 for r in results if r["status"] == "NEEDS HUMAN")
    total_count = len(results)
    success_rate = round(((auto_count + retry_count) / total_count) * 100, 1) if total_count else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>🟢 Auto Resolved</div><div class='metric-val'>{auto_count}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>🟠 Resolved After Retry</div><div class='metric-val'>{retry_count}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>🔴 Needs Attention</div><div class='metric-val'>{human_count}</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-card'><div class='metric-label'>✨ AI Success Rate</div><div class='metric-val'>{success_rate}%</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Toolbar
    tcols = st.columns(2)
    
    possible_report_paths = [
        repo_path / "MERGEMIND_REPORT.md",
        Path("demo_repo/MERGEMIND_REPORT.md").resolve(),
        Path("MERGEMIND_REPORT.md").resolve()
    ]
    
    report_text = ""
    for rp in possible_report_paths:
        if rp.exists():
            try:
                report_text = rp.read_text(encoding="utf-8")
                break
            except Exception:
                pass

    if report_text:
        tcols[0].download_button("📥 Export Audit Report (.md)", data=report_text, file_name="MERGEMIND_REPORT.md", use_container_width=True)
    else:
        tcols[0].download_button("📥 Export Audit Report (.md)", data="Audit Log", file_name="MERGEMIND_REPORT.md", use_container_width=True)

    if tcols[1].button("✅ Finalize & Commit Git Merge", type="secondary", use_container_width=True):
        unresolved = [r for r in results if r["status"] == "NEEDS HUMAN"]
        if unresolved:
            st.warning(f"Please resolve the remaining {len(unresolved)} 'NEEDS HUMAN' conflict(s) below before committing!")
        else:
            success, msg = finalize_git_merge(str(repo_path))
            if success:
                st.balloons()
                st.success("Git merge committed successfully! " + msg)
            else:
                st.error("Merge commit error: " + msg)

    st.markdown("---")
    st.markdown("### 🔍 Conflicted File Intelligence Studio")

    for idx, item in enumerate(results):
        file_path = item["file_path"]
        status = item["status"]
        confidence = item["confidence"]
        reasoning = item["reasoning"]
        language = item.get("language", "Code")

        badge_class = "badge-auto" if status in ["AUTO-RESOLVED", "HUMAN-RESOLVED"] else ("badge-retry" if status == "RESOLVED AFTER RETRY" else "badge-human")
        badge_text = f"🟢 {status}" if status == "AUTO-RESOLVED" else (f"🟠 {status}" if status == "RESOLVED AFTER RETRY" else f"🔴 {status}")

        with st.expander(f"📁 {file_path} ({language}) — {status} ({confidence}% Confidence)", expanded=(status == "NEEDS HUMAN")):
            st.markdown(f"**Language:** `{language}` &nbsp;|&nbsp; **Status:** <span class='status-badge {badge_class}'>{badge_text}</span>", unsafe_allow_html=True)
            st.markdown(f"**AI Rationale:** {reasoning}")

            tabs = st.tabs(["💡 Intent Analysis", "🔄 Execution Trail", "🔍 Code Diff", "🧪 Test Logs", "👤 Manual Decision Studio"])

            # TAB 1: Intent Analysis Visualizer
            with tabs[0]:
                st.markdown("##### Side-by-Side Intention Comparison")
                analysis = item.get("analysis", {})
                
                ic1, ic2 = st.columns(2)
                with ic1:
                    st.markdown("""
                    <div class="intent-card intent-ours">
                        <div class="intent-header" style="color: #3B82F6;">🔹 OURS (HEAD Branch) Intent</div>
                        <div>""" + str(analysis.get("ours_intent")) + """</div>
                    </div>
                    """, unsafe_allow_html=True)
                with ic2:
                    st.markdown("""
                    <div class="intent-card intent-theirs">
                        <div class="intent-header" style="color: #8B5CF6;">🔸 THEIRS (Feature Branch) Intent</div>
                        <div>""" + str(analysis.get("theirs_intent")) + """</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                st.info(f"**Conflict Classification:** {analysis.get('conflict_nature')}")

            # TAB 2: Execution Trail
            with tabs[1]:
                history = item.get("history", [])
                for h in history:
                    attempt_num = h["attempt"]
                    st.markdown(f"**Attempt #{attempt_num} — Confidence: {h['confidence']}%**")
                    st.write(f"Reasoning: {h['reasoning']}")
                    with st.expander(f"View Proposed Code (Attempt #{attempt_num})"):
                        st.code(h["merged_code"], language=language.lower())

                if status == "NEEDS HUMAN":
                    st.error(f"Escalated to Human Engineer: {reasoning}")

            # TAB 3: Diff View
            with tabs[2]:
                st.markdown("##### Code Modifications")
                initial = item["initial_content"].splitlines()
                final = item["final_content"].splitlines()
                diff = list(difflib.unified_diff(initial, final, fromfile="Original (Conflicted)", tofile="Resolved", lineterm=""))
                if diff:
                    st.code("\n".join(diff), language="diff")
                else:
                    st.info("File currently in original conflicted state awaiting decision.")

            # TAB 4: Verification Logs
            with tabs[3]:
                st.markdown(f"##### Test Suite Output ({language})")
                log_file = repo_path / "mergemind_log.json"
                if log_file.exists():
                    try:
                        log_data = json.loads(log_file.read_text(encoding="utf-8"))
                        file_verify_logs = [l for l in log_data if l.get("file_path") == file_path and l.get("step") == "VERIFY"]
                        for vl in file_verify_logs:
                            details = vl.get("details", {})
                            st.write(f"**Unit Tests Passed:** `{details.get('existing_tests_passed')}`")
                            st.write(f"**Dynamic Behavior Check:** `{details.get('gen_test_passed')}`")
                            st.code(details.get("pytest_output", "No log output recorded"), language="text")
                    except Exception as le:
                        st.warning(f"Could not parse log data: {le}")

            # TAB 5: Manual Decision Editor
            with tabs[4]:
                st.markdown("##### Interactive Decision Studio")
                if status not in ["NEEDS HUMAN"]:
                    st.success(f"File automatically resolved! Resolved {language} code:")
                    st.code(item["final_content"], language=language.lower())
                else:
                    st.warning("Conflict requires explicit human decision. Choose or edit final code:")
                    
                    from mergemind.parser import parse_conflict_file
                    file_data = parse_conflict_file(repo_path / file_path)
                    ours_option = file_data["conflicts"][0]["ours_code"] if file_data["conflicts"] else ""
                    theirs_option = file_data["conflicts"][0]["theirs_code"] if file_data["conflicts"] else ""

                    choice = st.radio(
                        f"Select branch variant for {file_path}:",
                        ["Keep Ours (HEAD)", "Keep Theirs (FEATURE)", "Custom Editor"],
                        key=f"radio_{idx}"
                    )

                    if choice == "Keep Ours (HEAD)":
                        resolved_code = ours_option
                    elif choice == "Keep Theirs (FEATURE)":
                        resolved_code = theirs_option
                    else:
                        resolved_code = st.text_area("Custom Code Editor:", value=item["initial_content"], height=220, key=f"text_{idx}")

                    if st.button(f"Save & Mark Resolved ({file_path})", key=f"btn_{idx}"):
                        (repo_path / file_path).write_text(resolved_code, encoding="utf-8")
                        st.success(f"File `{file_path}` marked as resolved!")
                        item["status"] = "HUMAN-RESOLVED"
                        item["final_content"] = resolved_code
                        st.rerun()

else:
    st.info("Select '🔄 Reset Demo Repository' and '🚀 Analyze & Resolve Conflicts' in the sidebar to run the studio.")
