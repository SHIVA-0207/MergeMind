import re
from pathlib import Path
from typing import Dict, List, Any
import git

def get_conflicted_files(repo_path: Path) -> List[str]:
    """Find list of relative file paths currently in git conflict state."""
    repo = git.Repo(repo_path)
    unmerged = repo.index.unmerged_blobs()
    return list(unmerged.keys())

def get_commit_context(repo_path: Path, max_count: int = 5) -> Dict[str, List[str]]:
    """Retrieve recent commit messages for HEAD and MERGE_HEAD."""
    repo = git.Repo(repo_path)
    ours_logs = []
    theirs_logs = []
    
    try:
        for c in repo.iter_commits("HEAD", max_count=max_count):
            ours_logs.append(f"{c.hexsha[:7]}: {c.summary}")
    except Exception as e:
        ours_logs.append(f"Error fetching HEAD commits: {e}")
        
    try:
        for c in repo.iter_commits("MERGE_HEAD", max_count=max_count):
            theirs_logs.append(f"{c.hexsha[:7]}: {c.summary}")
    except Exception as e:
        theirs_logs.append("MERGE_HEAD logs unavailable")
        
    return {
        "ours_commits": ours_logs,
        "theirs_commits": theirs_logs
    }

def parse_conflict_file(file_path: Path) -> Dict[str, Any]:
    """
    Parse a file containing git merge conflict markers.
    Extracts OURS, THEIRS, and overall context.
    """
    content = file_path.read_text(encoding="utf-8")
    
    pattern = re.compile(
        r'<<<<<<< (.*?)\n(.*?)\n=======\n(.*?)\n>>>>>>> (.*?)\n',
        re.DOTALL
    )
    
    conflicts = []
    matches = list(pattern.finditer(content))
    
    for idx, match in enumerate(matches):
        ours_label = match.group(1).strip()
        ours_code = match.group(2)
        theirs_code = match.group(3)
        theirs_label = match.group(4).strip()
        
        conflicts.append({
            "block_index": idx + 1,
            "ours_label": ours_label,
            "ours_code": ours_code,
            "theirs_label": theirs_label,
            "theirs_code": theirs_code,
            "full_marker_text": match.group(0)
        })
        
    return {
        "file_path": str(file_path),
        "raw_content": content,
        "conflicts": conflicts,
        "has_conflicts": len(conflicts) > 0
    }
