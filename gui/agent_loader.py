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
        
        # Ensure examples directory exists
        try:
            self.examples_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return False, f"Error creating examples directory: {e}"
        
        file_path = self.examples_dir / filename
        
        # Check if file already exists (don't allow overwrite in save)
        if file_path.exists():
            return False, f"File {filename} already exists. Choose a different name or delete the existing one first."
        
        try:
            file_path.write_text(code, encoding='utf-8')
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
        if filename.startswith('0'):
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
        if not new_filename.endswith('.py'):
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
            code = source_path.read_text(encoding='utf-8')
            
            # Update class name in duplicated code
            import re
            # Extract original class name
            match = re.search(r'class\s+(\w+)\(Agent\)', code)
            if match:
                old_class = match.group(1)
                # Create new class name from filename
                new_class = ''.join(word.capitalize() for word in new_filename[:-3].split('_'))
                # Replace class name
                code = code.replace(f'class {old_class}', f'class {new_class}')
                code = code.replace(f'{old_class}()', f'{new_class}()')
            
            dest_path.write_text(code, encoding='utf-8')
            return True, f"✅ Duplicated to {new_filename}"
        except Exception as e:
            return False, f"Error duplicating file: {e}"
    
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
            if 'RAGConfig' in content or 'self.rag' in content:
                agent_type = "RAG-Powered"
            elif 'LLMConfig' in content or 'self.llm' in content:
                agent_type = "LLM-Powered"
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
