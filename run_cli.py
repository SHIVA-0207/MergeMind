import sys
from pathlib import Path
from create_demo_repo import setup_demo_repository
from mergemind.agent import process_repository

def main():
    print("=" * 60)
    print("🤖 MERGEMIND: AGENTIC AI GIT MERGE CONFLICT RESOLVER (CLI)")
    print("=" * 60)
    
    print("\n[STEP 1] Generating Demo Git Repository with 3 Merge Conflicts...")
    setup_demo_repository()
    
    demo_dir = Path("demo_repo").resolve()
    
    print("\n[STEP 2] Running MergeMind 5-Step Agentic Loop...")
    print("         (ANALYZE -> PLAN & ACT -> VERIFY -> RE-PLAN -> ESCALATE)")
    print("-" * 60)
    
    results = process_repository(str(demo_dir))
    
    print("\n" + "=" * 60)
    print("📊 MERGEMIND CONFLICT RESOLUTION SUMMARY")
    print("=" * 60)
    
    for item in results:
        file_path = item["file_path"]
        status = item["status"]
        confidence = item["confidence"]
        reasoning = item["reasoning"]
        
        status_icon = "🟢" if status == "AUTO-RESOLVED" else ("🟠" if status == "RESOLVED AFTER RETRY" else "🔴")
        
        print(f"\n📁 File: {file_path}")
        print(f"   Status:     {status_icon} {status}")
        print(f"   Confidence: {confidence}%")
        print(f"   Reasoning:  {reasoning}")
        print("   " + "-" * 50)
        
        analysis = item.get("analysis", {})
        print(f"   • Ours Intent:   {analysis.get('ours_intent')}")
        print(f"   • Theirs Intent: {analysis.get('theirs_intent')}")
        print(f"   • Nature:        {analysis.get('conflict_nature')}")

    print("\n" + "=" * 60)
    print("✅ AGENT LOOP COMPLETED SUCCESSFULLY IN TERMINAL!")
    print("=" * 60)

if __name__ == "__main__":
    main()
