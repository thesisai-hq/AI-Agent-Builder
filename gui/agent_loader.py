"""Agent Loader - Load and manage agents from examples/ directory

DESIGN PRINCIPLE: One agent class per file for maximum clarity.

This simplifies loading, testing, and management while providing
the best educational experience for students.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AgentLoader:
    """Loads and manages agents from the examples directory.

    Expects ONE agent class per file for simplicity and clarity.
    """

    def __init__(self, examples_dir: Path):
        """Initialize loader with examples directory path.

        Args:
            examples_dir: Path to examples/ directory
        """
        self.examples_dir = Path(examples_dir)
        if not self.examples_dir.exists():
            self.examples_dir.mkdir(parents=True, exist_ok=True)

    def list_agents(self) -> List[Dict[str, str]]:
        """List all agent files in examples/ directory.

        Returns ONE agent per file (first Agent class found).

        Returns:
            List of dicts with agent info (name, filename, type)
        """
        agents = []

        for file_path in self.examples_dir.glob("*.py"):
            # Skip __init__.py and other special files
            if file_path.name.startswith("_"):
                continue

            # Parse file to extract agent info (first agent only)
            agent_info = self._parse_agent_file(file_path)
            if agent_info:
                agents.append(agent_info)

        return sorted(agents, key=lambda x: x["filename"])

    def get_agent_code(self, filename: str) -> str:
        """Get the source code of an agent.

        Args:
            filename: Agent filename

        Returns:
            Agent source code
        """
        file_path = self.examples_dir / filename

        if not file_path.exists():
            return f"# Error: File {filename} not found"

        try:
            return file_path.read_text()
        except Exception as e:
            return f"# Error reading file: {e}"

    def save_agent(self, filename: str, code: str) -> Tuple[bool, str]:
        """Save agent code to examples/ directory.

        Args:
            filename: Filename to save as
            code: Agent source code

        Returns:
            Tuple of (success, message)
        """
        # Validate filename
        if not filename.endswith(".py"):
            return False, "Filename must end with .py"

        if not self._is_valid_filename(filename):
            return False, "Invalid filename. Use only letters, numbers, and underscores"

        # Ensure examples directory exists
        try:
            self.examples_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return False, f"Error creating examples directory: {e}"

        file_path = self.examples_dir / filename

        # Check if file already exists (don't allow overwrite in save)
        if file_path.exists():
            return (
                False,
                f"File {filename} already exists. Choose a different name or delete the existing one first.",
            )

        try:
            file_path.write_text(code, encoding="utf-8")
            # Verify file was written
            if file_path.exists():
                return True, f"✅ Agent saved to {file_path.relative_to(file_path.parent.parent)}"
            else:
                return False, "File write succeeded but file not found"
        except Exception as e:
            return False, f"Error saving file: {type(e).__name__}: {e}"

    def delete_agent(self, filename: str) -> Tuple[bool, str]:
        """Delete an agent file.

        Args:
            filename: Filename to delete

        Returns:
            Tuple of (success, message)
        """
        file_path = self.examples_dir / filename

        if not file_path.exists():
            return False, f"File {filename} not found"

        # Don't delete framework example files
        if filename.startswith("0"):
            return False, "Cannot delete framework example files (01_*.py, 02_*.py, etc.)"

        try:
            file_path.unlink()
            return True, f"✅ Deleted {filename}"
        except Exception as e:
            return False, f"Error deleting file: {e}"

    def duplicate_agent(self, filename: str, new_filename: str) -> Tuple[bool, str]:
        """Duplicate an agent file.

        Args:
            filename: Original filename
            new_filename: New filename for the copy

        Returns:
            Tuple of (success, message)
        """
        # Validate new filename
        if not new_filename.endswith(".py"):
            return False, "Filename must end with .py"

        if not self._is_valid_filename(new_filename):
            return False, "Invalid filename. Use only letters, numbers, and underscores"

        source_path = self.examples_dir / filename
        dest_path = self.examples_dir / new_filename

        if not source_path.exists():
            return False, f"Source file {filename} not found"

        if dest_path.exists():
            return False, f"File {new_filename} already exists. Choose a different name."

        try:
            # Read source and write to destination
            code = source_path.read_text(encoding="utf-8")

            # Update class name in duplicated code
            import re

            # Extract original class name
            match = re.search(r"class\s+(\w+)\(Agent\)", code)
            if match:
                old_class = match.group(1)
                # Create new class name from filename
                new_class = "".join(word.capitalize() for word in new_filename[:-3].split("_"))
                # Replace class name
                code = code.replace(f"class {old_class}", f"class {new_class}")
                code = code.replace(f"{old_class}()", f"{new_class}()")

            dest_path.write_text(code, encoding="utf-8")
            return True, f"✅ Duplicated to {new_filename}"
        except Exception as e:
            return False, f"Error duplicating file: {e}"

    def _parse_agent_file(self, file_path: Path) -> Optional[Dict[str, str]]:
        """Parse agent file to extract metadata for ONE agent class.

        DESIGN: One agent per file for clarity and simplicity.
        If multiple agents found, returns FIRST one only with warning.

        Args:
            file_path: Path to agent file

        Returns:
            Dict with agent info, or None if parsing fails
        """
        try:
            content = file_path.read_text()

            # Find FIRST agent class (one per file principle)
            match = re.search(r"class\s+(\w+)\(Agent\)", content)

            if not match:
                return None

            agent_name = match.group(1)

            # Skip base/abstract classes
            if agent_name in ["BaseAgent", "AbstractAgent"]:
                return None

            # Determine agent type based on code patterns
            # Check in order: RAG → Hybrid → LLM → Rule-Based

            has_rag = "RAGConfig" in content or "self.rag" in content
            has_llm = "LLMConfig" in content or "self.llm" in content
            has_rules = self._has_rule_logic(content)

            if has_rag:
                agent_type = "RAG-Powered"
            elif has_llm and has_rules:
                agent_type = "Hybrid"  # Both LLM and rules!
            elif has_llm:
                agent_type = "LLM-Powered"
            else:
                agent_type = "Rule-Based"

            # Check if file has multiple agents (warning case)
            all_matches = re.findall(r"class\s+(\w+)\(Agent\)", content)
            agent_count = len(
                [name for name in all_matches if name not in ["BaseAgent", "AbstractAgent"]]
            )

            if agent_count > 1:
                # Multiple agents found - add warning to name
                agent_name = f"{agent_name} ⚠️ (+{agent_count - 1} more in file)"

            return {"name": agent_name, "filename": file_path.name, "type": agent_type}

        except Exception:
            return None

    @staticmethod
    def _has_rule_logic(content: str) -> bool:
        """Detect if agent has intentional rule-based logic in analyze method.

        Distinguishes between:
        - Primary rule-based logic (hybrid agent)
        - Fallback exception handling (LLM agent safety net)

        Args:
            content: File content

        Returns:
            True if intentional rule-based logic detected (not just fallback)
        """
        # Look for analyze method
        analyze_match = re.search(
            r"async def analyze\(self.*?\):.*?(?=\n    def |\n\nclass |\n\nasync |$)",
            content,
            re.DOTALL,
        )

        if not analyze_match:
            return False

        analyze_code = analyze_match.group(0)

        # Check if rules are in try/except block (fallback, not primary logic)
        # If there's a try block before the rules, it's likely fallback
        has_try_block = "try:" in analyze_code

        # Check for rule patterns
        rule_patterns = [
            r"if\s+.*?data\.get\(",  # if data.get('pe_ratio')
            r"elif\s+.*?data\.get\(",  # elif data.get('growth')
            r"if\s+\w+\s*[<>=!]+\s*\d+",  # if pe < 15
            r"data\.get\(['\"]\w+['\"].*?[<>=!]",  # data.get('pe') < 15
        ]

        has_rules = any(re.search(pattern, analyze_code) for pattern in rule_patterns)

        if not has_rules:
            return False

        # If has try block, check if rules are BEFORE the try (primary logic)
        # or INSIDE except (fallback logic)
        if has_try_block:
            # Split into try and except sections
            try_match = re.search(r"try:(.*?)except", analyze_code, re.DOTALL)
            if try_match:
                try_section = try_match.group(1)
                # If rules are in try section (before LLM call), it's hybrid
                # If rules are NOT in try section (in except), it's just fallback
                return any(re.search(pattern, try_section) for pattern in rule_patterns)

            # Has try but couldn't parse - assume it's fallback (LLM agent)
            return False

        # No try block - rules are primary logic (hybrid or rule-based)
        return True

    @staticmethod
    def _is_valid_filename(filename: str) -> bool:
        """Check if filename is valid.

        Args:
            filename: Filename to validate

        Returns:
            True if valid
        """
        # Remove .py extension for checking
        name = filename[:-3] if filename.endswith(".py") else filename

        # Must start with letter, contain only alphanumeric and underscores
        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", name))
