import json
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    "project_name": "MergeMind Managed Workspace",
    "confidence_threshold": 70,
    "max_retry_attempts": 3,
    "preferred_strategy": "smart_merge",
    "strict_test_verification": True,
    "supported_languages": [".py", ".js", ".ts", ".go", ".java", ".cpp"]
}

def load_team_config(repo_path: Path) -> Dict[str, Any]:
    """
    Loads team configuration from .mergemind.json if present in the repository root.
    """
    config_file = repo_path / ".mergemind.json"
    if config_file.exists():
        try:
            user_config = json.loads(config_file.read_text(encoding="utf-8"))
            merged = DEFAULT_CONFIG.copy()
            merged.update(user_config)
            return merged
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()
