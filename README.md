# MergeMind 🤖

**MergeMind** is an agentic AI system designed to resolve Git merge conflicts intelligently. It reads conflict markers, analyzes commit history and side intentions using Gemini LLM, proposes merged code, verifies the merge with `pytest` and dynamic behavior tests, retries on test failure, and escalates ambiguous or low-confidence conflicts to human engineers with a Streamlit UI.

---

## 🎯 Features

- **Agentic Loop**:
  1. **ANALYZE**: Parses conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>>`) and queries Gemini to summarize the intent of both sides.
  2. **PLAN AND ACT**: Proposes merged code along with a confidence score (0–100).
  3. **VERIFY**: Runs `pytest` on the merged codebase and generates a dynamic micro-behavior test verifying both intentions.
  4. **RE-PLAN**: On verification failure, feeds the error logs back into Gemini for up to 3 retry attempts.
  5. **ESCALATE**: If confidence is <70 or max retries are exceeded, marks the file `NEEDS HUMAN` with plain-English explanation.
- **Streamlit Web UI**:
  - Interactive status badges (`AUTO-RESOLVED`, `RESOLVED AFTER RETRY`, `NEEDS HUMAN`).
  - Step-by-step reasoning trail timeline for each file.
  - Before vs After code diff visualization.
  - Pytest verification logs & generated test display.
  - Interactive Human Resolution panel to choose Ours, Theirs, or custom edit.
- **Demo Repository Script**:
  - Generates a local Git repository with 3 realistic conflict cases (Easy, Medium, Impossible).

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.11+
- Git installed on system PATH

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and set your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

---

## 💻 Running the Demo & Streamlit UI

### Step 1: Create the Demo Repository
Generate the demo repository containing 3 git merge conflicts:
```bash
python create_demo_repo.py
```
This initializes `./demo_repo` with:
1. `easy_module.py` (Easy: auto-resolves on attempt 1)
2. `medium_module.py` (Medium: resolves after retry on attempt 2)
3. `impossible_module.py` (Impossible: escalates to `NEEDS HUMAN`)

### Step 2: Launch the Web UI
Start the Streamlit application:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### Step 3: Run MergeMind Agent
In the Streamlit sidebar:
1. Ensure the Git Repository Path points to `./demo_repo`.
2. Click **"🚀 Run MergeMind Agent"**.
3. View the reasoning trails, confidence scores, test logs, diffs, and interactively resolve human-escalated cases.

---

## 📂 Project Structure

```
charming-hawking/
├── app.py                   # Streamlit Web UI dashboard
├── create_demo_repo.py      # Demo Git repository generator script
├── mergemind/               # Agentic core package
│   ├── __init__.py
│   ├── parser.py            # Git conflict marker & commit context parser
│   └── agent.py             # 5-step Agent Loop logic & Gemini integration
├── mergemind_log.json       # JSON execution log file
├── requirements.txt         # Project dependencies
├── .env.example             # Environment template
└── README.md                # Project documentation
```
