"""
Security Audit Script - Run before committing
"""

import os
import re
import sys


def check_hardcoded_credentials():
    """Check for hardcoded credentials in code"""
    print("🔍 Checking for hardcoded credentials...")

    issues = []
    patterns = [
        (r'password\s*=\s*["\'](?!.*\$|.*getenv)[^"\']+["\']', "Hardcoded password"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
        (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret"),
        (r"postgresql://[^:]+:[^@]+@", "Credentials in connection string"),
    ]

    for root, dirs, files in os.walk("agent_builder"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    content = f.read()
                    for pattern, issue_type in patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            issues.append(f"{filepath}: {issue_type}")

    if issues:
        print("❌ Found credential issues:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("   ✅ No hardcoded credentials found")
        return True


def check_env_in_git():
    """Check if .env is excluded from git"""
    print("\n🔍 Checking .gitignore...")

    if not os.path.exists(".gitignore"):
        print("   ❌ .gitignore missing!")
        return False

    with open(".gitignore", "r") as f:
        content = f.read()

    if ".env" in content:
        print("   ✅ .env excluded from git")
        return True
    else:
        print("   ❌ .env not in .gitignore!")
        return False


def check_sql_injection():
    """Check for SQL injection vulnerabilities"""
    print("\n🔍 Checking for SQL injection risks...")

    issues = []

    # Check repository.py for table validation
    repo_file = "agent_builder/repositories/repository.py"
    if os.path.exists(repo_file):
        with open(repo_file, "r") as f:
            content = f.read()

        if "validate_table_name" in content:
            print("   ✅ Table name validation present")
        else:
            issues.append("repository.py: Missing table name validation")

    if issues:
        print("   ❌ Found SQL injection risks:")
        for issue in issues:
            print(f"      - {issue}")
        return False
    else:
        print("   ✅ No obvious SQL injection vulnerabilities")
        return True


def check_required_files():
    """Check for required open source files"""
    print("\n🔍 Checking required files...")

    required = {
        "LICENSE": "License file",
        "README.md": "Project documentation",
        ".env.example": "Environment template",
        "CONTRIBUTING.md": "Contribution guidelines",
    }

    missing = []
    for file, desc in required.items():
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            missing.append(f"{file} - {desc}")

    if missing:
        print("   ⚠️  Missing files:")
        for item in missing:
            print(f"      - {item}")
        return False

    return True


def main():
    """Run security audit"""
    print("=" * 60)
    print("🛡️  Security Audit for Open Source Release")
    print("=" * 60)

    checks = [
        check_hardcoded_credentials(),
        check_env_in_git(),
        check_sql_injection(),
        check_required_files(),
    ]

    print("\n" + "=" * 60)

    if all(checks):
        print("✅ ALL SECURITY CHECKS PASSED!")
        print("=" * 60)
        print("\n🎉 Ready for public GitHub release!")
        return 0
    else:
        print("❌ SECURITY ISSUES FOUND!")
        print("=" * 60)
        print("\n⚠️  DO NOT commit to public repo until fixed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
