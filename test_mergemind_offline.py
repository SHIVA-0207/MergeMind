import sys
from pathlib import Path
from create_demo_repo import setup_demo_repository
from mergemind.parser import get_conflicted_files, parse_conflict_file, get_commit_context

def test_demo_and_parser():
    print("Step 1: Setting up demo repository...")
    setup_demo_repository()
    
    demo_dir = Path("demo_repo").resolve()
    conflicted_files = get_conflicted_files(demo_dir)
    print(f"Conflicted files found by GitPython: {conflicted_files}")
    assert len(conflicted_files) == 3, f"Expected 3 conflicted files, found {len(conflicted_files)}"
    
    for f in conflicted_files:
        full_p = demo_dir / f
        parsed = parse_conflict_file(full_p)
        print(f"\n--- Parsed {f} ---")
        print(f"Has conflicts: {parsed['has_conflicts']}")
        print(f"Conflict count: {len(parsed['conflicts'])}")
        assert parsed['has_conflicts'] is True
        for c in parsed['conflicts']:
            print(f"  Block {c['block_index']}: OURS ({c['ours_label']}) vs THEIRS ({c['theirs_label']})")
            
    commit_ctx = get_commit_context(demo_dir)
    print("\n--- Commit Context ---")
    print("OURS Commits:", commit_ctx["ours_commits"])
    print("THEIRS Commits:", commit_ctx["theirs_commits"])
    
    print("\n✅ All demo creation and conflict parsing checks passed successfully!")

if __name__ == "__main__":
    test_demo_and_parser()
