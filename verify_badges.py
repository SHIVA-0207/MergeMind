from pathlib import Path
from create_demo_repo import setup_demo_repository
from mergemind.agent import process_repository

def run_test():
    print("Setting up demo repository...")
    setup_demo_repository()
    
    demo_dir = Path("demo_repo").resolve()
    print("Running MergeMind Agent process_repository...")
    results = process_repository(str(demo_dir))
    
    print("\n=== AGENT RESULTS SUMMARY ===")
    for r in results:
        print(f"File: {r['file_path']} | Status: {r['status']} | Confidence: {r['confidence']}%")
        print(f"Reasoning: {r['reasoning']}\n")

if __name__ == "__main__":
    run_test()
