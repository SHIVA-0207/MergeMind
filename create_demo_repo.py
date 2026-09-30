import os
import shutil
import subprocess
import sys
from pathlib import Path

DEMO_DIR = Path("demo_repo").resolve()

def run_git(args, cwd=DEMO_DIR):
    cmd = ["git"] + args
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0 and "merge" not in args:
        print(f"Git command failed: {' '.join(cmd)}\nStderr: {res.stderr}")
        sys.exit(1)
    return res

def setup_demo_repository():
    print(f"Creating NEW demo repository at: {DEMO_DIR}")
    
    if DEMO_DIR.exists():
        for root, dirs, files in os.walk(DEMO_DIR):
            for fname in files:
                try:
                    os.chmod(os.path.join(root, fname), 0o777)
                except Exception:
                    pass
        try:
            shutil.rmtree(DEMO_DIR, ignore_errors=True)
        except Exception:
            pass

    DEMO_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize Git
    run_git(["init"])
    run_git(["config", "user.name", "MergeMind Demo"])
    run_git(["config", "user.email", "demo@mergemind.ai"])
    run_git(["checkout", "-b", "main"])

    # 1. Base Files
    # Auth Base
    auth_base = '''def authenticate_user(email, password):
    # Base authentication logic
    user = {"email": email, "authenticated": True}
    return user
'''
    test_auth = '''from auth_service import authenticate_user

def test_authenticate_user():
    user = authenticate_user("test@company.com", "secret123")
    assert user["authenticated"] is True
    assert user.get("hashed") is True
'''

    # Payment Base
    payment_base = '''def process_payment(amount, currency):
    # Base payment processing
    total = amount * 1.0
    return round(total, 2)
'''
    test_payment = '''import pytest
from payment_processor import process_payment

def test_payment_standard():
    assert process_payment(100.0, "USD", fee=5.0) == 105.0

def test_payment_validation():
    with pytest.raises(ValueError):
        process_payment(-10.0, "USD", fee=5.0)
'''

    # Shipping Base (Impossible)
    shipping_base = '''FREE_SHIPPING_THRESHOLD = 75.00

def qualifies_for_free_shipping(order_total):
    return order_total >= FREE_SHIPPING_THRESHOLD
'''
    test_shipping = '''from shipping_config import qualifies_for_free_shipping

def test_shipping():
    assert qualifies_for_free_shipping(200.0) is True
'''

    # JS API Router Base
    js_api_base = '''function handleRequest(req, res) {
    res.status = 200;
    return res;
}

module.exports = { handleRequest };
'''

    (DEMO_DIR / "auth_service.py").write_text(auth_base, encoding="utf-8")
    (DEMO_DIR / "test_auth.py").write_text(test_auth, encoding="utf-8")
    
    (DEMO_DIR / "payment_processor.py").write_text(payment_base, encoding="utf-8")
    (DEMO_DIR / "test_payment.py").write_text(test_payment, encoding="utf-8")

    (DEMO_DIR / "shipping_config.py").write_text(shipping_base, encoding="utf-8")
    (DEMO_DIR / "test_shipping.py").write_text(test_shipping, encoding="utf-8")

    (DEMO_DIR / "api_router.js").write_text(js_api_base, encoding="utf-8")

    run_git(["add", "."])
    run_git(["commit", "-m", "Initial commit with E-Commerce microservices"])

    # Create feature branch
    run_git(["checkout", "-b", "feature-branch"])

    # Feature branch edits:
    auth_feature = '''def authenticate_user(email, password):
    # Feature branch: email domain validation
    if not email.endswith("@company.com"):
        raise ValueError("Only company email addresses allowed")
    user = {"email": email, "authenticated": True}
    return user
'''
    (DEMO_DIR / "auth_service.py").write_text(auth_feature, encoding="utf-8")

    payment_feature = '''def process_payment(amount, currency, fee=0.0):
    # Feature branch: transaction fee support
    total = (amount + fee) * 1.0
    return round(total, 2)
'''
    (DEMO_DIR / "payment_processor.py").write_text(payment_feature, encoding="utf-8")

    shipping_feature = '''# Feature branch requirement: Holiday Promo lowered threshold to $50
FREE_SHIPPING_THRESHOLD = 50.00

def qualifies_for_free_shipping(order_total):
    return order_total >= FREE_SHIPPING_THRESHOLD
'''
    (DEMO_DIR / "shipping_config.py").write_text(shipping_feature, encoding="utf-8")

    js_feature = '''function handleRequest(req, res) {
    // Feature branch: Rate limiting header
    res.setHeader("X-RateLimit-Limit", "100");
    res.status = 200;
    return res;
}

module.exports = { handleRequest };
'''
    (DEMO_DIR / "api_router.js").write_text(js_feature, encoding="utf-8")

    run_git(["add", "."])
    run_git(["commit", "-m", "Feature branch: email validation, transaction fee, holiday promo $50, rate limit"])

    # Switch back to main branch
    run_git(["checkout", "main"])

    # Main branch edits:
    auth_main = '''def authenticate_user(email, password):
    # Base authentication logic
    user = {"email": email, "authenticated": True}
    # Main branch: Password hashing flag
    user["hashed"] = True
    return user
'''
    (DEMO_DIR / "auth_service.py").write_text(auth_main, encoding="utf-8")

    payment_main = '''def process_payment(amount, currency):
    # Main branch: Amount validation check
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    total = amount * 1.0
    return round(total, 2)
'''
    (DEMO_DIR / "payment_processor.py").write_text(payment_main, encoding="utf-8")

    shipping_main = '''# Main branch requirement: Standard enterprise threshold $100
FREE_SHIPPING_THRESHOLD = 100.00

def qualifies_for_free_shipping(order_total):
    return order_total >= FREE_SHIPPING_THRESHOLD
'''
    (DEMO_DIR / "shipping_config.py").write_text(shipping_main, encoding="utf-8")

    js_main = '''function handleRequest(req, res) {
    // Main branch: CORS header
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.status = 200;
    return res;
}

module.exports = { handleRequest };
'''
    (DEMO_DIR / "api_router.js").write_text(js_main, encoding="utf-8")

    run_git(["add", "."])
    run_git(["commit", "-m", "Main branch: password hash flag, amount validation, standard threshold $100, CORS header"])

    # Merge feature-branch into main -> causes new conflicts!
    print("Attempting 'git merge feature-branch' on main...")
    run_git(["merge", "feature-branch"])

if __name__ == "__main__":
    setup_demo_repository()
