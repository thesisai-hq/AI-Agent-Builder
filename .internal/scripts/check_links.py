#!/usr/bin/env python3
"""
Link Checker for AI-Agent-Builder Documentation
Verifies all markdown links and reports broken ones.
"""

import re
from pathlib import Path
from typing import List, Tuple


class LinkChecker:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.broken_links = []
        self.valid_links = []
        self.external_links = []

    def extract_links(self, content: str, file_path: Path) -> List[Tuple[str, str]]:
        """Extract markdown links from content."""
        # Pattern: [text](link)
        pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
        matches = re.findall(pattern, content)
        return [(text, link) for text, link in matches]

    def check_link(self, link: str, source_file: Path) -> Tuple[bool, str]:
        """Check if a link is valid."""
        # Skip anchors (they're within the same file)
        if link.startswith("#"):
            return True, "anchor"

        # External links (http/https)
        if link.startswith("http://") or link.startswith("https://"):
            self.external_links.append((link, source_file))
            return True, "external"

        # Handle relative paths
        if link.startswith("../"):
            # Relative to parent directory
            target = (source_file.parent.parent / link.replace("../", "")).resolve()
        elif link.startswith("./"):
            # Relative to current directory
            target = (source_file.parent / link.replace("./", "")).resolve()
        else:
            # Relative to current directory (no ./)
            target = (source_file.parent / link).resolve()

        # Check if file exists
        if target.exists():
            return True, "valid"
        else:
            return False, f"missing: {target}"

    def check_file(self, file_path: Path):
        """Check all links in a markdown file."""
        print(f"Checking: {file_path.relative_to(self.root_dir)}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        links = self.extract_links(content, file_path)

        for text, link in links:
            is_valid, status = self.check_link(link, file_path)

            if is_valid:
                self.valid_links.append((file_path, text, link, status))
            else:
                self.broken_links.append((file_path, text, link, status))
                print(f"  ❌ BROKEN: [{text}]({link}) - {status}")

    def check_all(self):
        """Check all markdown files in the repository."""
        md_files = list(self.root_dir.rglob("*.md"))
        md_files = [f for f in md_files if ".git" not in str(f)]

        print(f"Found {len(md_files)} markdown files to check\n")

        for md_file in sorted(md_files):
            self.check_file(md_file)
            print()

    def report(self):
        """Generate report of findings."""
        print("=" * 70)
        print("LINK CHECK REPORT")
        print("=" * 70)
        print()

        print("📊 Statistics:")
        print(f"  Total valid links: {len(self.valid_links)}")
        print(f"  Total broken links: {len(self.broken_links)}")
        print(f"  External links: {len(self.external_links)}")
        print()

        if self.broken_links:
            print("❌ BROKEN LINKS:")
            print()
            for file_path, text, link, status in self.broken_links:
                print(f"  File: {file_path.relative_to(self.root_dir)}")
                print(f"    Link: [{text}]({link})")
                print(f"    Issue: {status}")
                print()
        else:
            print("✅ NO BROKEN LINKS FOUND!")
            print()

        if self.external_links:
            print("🌐 EXTERNAL LINKS (not checked):")
            print()
            unique_external = {}
            for link, source in self.external_links:
                if link not in unique_external:
                    unique_external[link] = []
                unique_external[link].append(source)

            for link in sorted(unique_external.keys()):
                print(f"  {link}")
                print(f"    Used in: {len(unique_external[link])} file(s)")
            print()

        print("=" * 70)

        return len(self.broken_links) == 0


if __name__ == "__main__":
    checker = LinkChecker(".")
    checker.check_all()
    all_valid = checker.report()

    exit(0 if all_valid else 1)
