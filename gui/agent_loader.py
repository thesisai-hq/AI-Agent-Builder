"""Agent Loader - Load and manage agents from examples/ directory"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class AgentLoader:
    """Loads and manages agents from the examples directory."""
    
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
        
        Returns:
            List of dicts with agent info (name, filename, type)
        """
        agents = []
        
        for file_path in self.examples_dir.glob("*.py"):
            # Skip __init__.py and other special files
            if file_path.name.startswith("_"):
                continue
            
            # Parse file to extract agent info
            agent_info = self._parse_agent_file(file_path)
            if agent_info:
                agents.append(agent_info)
        
        return sorted(agents, key=lambda x: x['filename'])
    
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
        if not filename.endswith('.py'):
            return False, "Filename must end with .py"
        
        if not self._is_valid_filename(filename):
            return False, "Invalid filename. Use only letters, numbers, and underscores"
        
        file_path = self.examples_dir / filename
        
        # Check if file already exists
        if file_path.exists():
            return False, f"File {filename} already exists. Choose a different name."
        
        try:
            file_path.write_text(code)
            return True, f"✅ Agent saved to examples/{filename}"
        except Exception as e:
            return False, f"Error saving file: {e}"
    
    def _parse_agent_file(self, file_path: Path) -> Optional[Dict[str, str]]:
        """Parse agent file to extract metadata.
        
        Args:
            file_path: Path to agent file
            
        Returns:
            Dict with agent info or None if parsing fails
        """
        try:
            content = file_path.read_text()
            
            # Extract agent class name (first class that inherits from Agent)
            class_match = re.search(r'class\s+(\w+)\(Agent\)', content)
            if not class_match:
                return None
            
            agent_name = class_match.group(1)
            
            # Determine agent type based on code patterns
            if 'LLMConfig' in content or 'self.llm' in content:
                agent_type = "LLM-Powered"
            elif 'RAGConfig' in content or 'self.rag' in content:
                agent_type = "RAG-Enabled"
            else:
                agent_type = "Rule-Based"
            
            return {
                'name': agent_name,
                'filename': file_path.name,
                'type': agent_type
            }
        except Exception:
            return None
    
    @staticmethod
    def _is_valid_filename(filename: str) -> bool:
        """Check if filename is valid.
        
        Args:
            filename: Filename to validate
            
        Returns:
            True if valid
        """
        # Remove .py extension for checking
        name = filename[:-3] if filename.endswith('.py') else filename
        
        # Must start with letter, contain only alphanumeric and underscores
        return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name))
