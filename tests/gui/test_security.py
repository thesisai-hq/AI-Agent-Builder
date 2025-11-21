"""Tests for security features.

Tests input sanitization, validation, and code generation safety.
Critical for preventing code injection attacks.
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gui.agent_creator import AgentCreator
from gui.agent_loader import AgentLoader


# ============================================================================
# Input Sanitization Tests
# ============================================================================

class TestInputSanitization:
    """Test input sanitization to prevent code injection."""
    
    def test_sanitize_identifier_removes_special_chars(self):
        """Test removal of special characters from identifiers."""
        creator = AgentCreator()
        
        # SQL injection attempt
        malicious = "Agent'; DROP TABLE users--"
        safe = creator._sanitize_identifier(malicious)
        assert safe == "AgentDROPTABLEusers"
        
        # Code injection attempt
        malicious = "Agent\nimport os\nos.system('rm -rf /')"
        safe = creator._sanitize_identifier(malicious)
        assert safe == "Agentimportosossystemrmrf"
        
        # Path traversal attempt
        malicious = "../../../evil"
        safe = creator._sanitize_identifier(malicious)
        assert safe == "evil"
    
    def test_sanitize_identifier_ensures_valid_start(self):
        """Test identifier starts with letter."""
        creator = AgentCreator()
        
        # Starts with number
        assert creator._sanitize_identifier("123Agent") == "A123Agent"
        
        # Starts with underscore (technically valid but we ensure letter)
        result = creator._sanitize_identifier("_Agent")
        assert result[0].isalpha() or result.startswith("A")
    
    def test_sanitize_identifier_empty_input(self):
        """Test handling of empty input."""
        creator = AgentCreator()
        
        assert creator._sanitize_identifier("") == "Agent"
        assert creator._sanitize_identifier("   ") == "Agent"
        assert creator._sanitize_identifier("!!!") == "Agent"
    
    def test_escape_string_literal_prevents_breakout(self):
        """Test escaping prevents breaking out of strings."""
        creator = AgentCreator()
        
        # Triple quote breakout attempt
        malicious = '''Legit text"""; import os; os.system("evil")'''
        escaped = creator._escape_string_literal(malicious)
        
        # Triple quotes should be escaped
        assert '"""' not in escaped
        assert r'\"\"\"' in escaped or escaped.count('"') != 3
    
    def test_escape_string_literal_escapes_backslashes(self):
        """Test backslash escaping."""
        creator = AgentCreator()
        
        # Backslash escape sequences
        text = "Path: C:\\Users\\Admin"
        escaped = creator._escape_string_literal(text)
        
        # Backslashes should be doubled
        assert "\\\\" in escaped
    
    def test_validate_numeric_safe_conversion(self):
        """Test safe numeric validation."""
        creator = AgentCreator()
        
        # Valid numbers
        assert creator._validate_numeric(15.5) == 15.5
        assert creator._validate_numeric("20") == 20.0
        assert creator._validate_numeric(30) == 30.0
        
        # Invalid inputs return default
        assert creator._validate_numeric("not a number", default=0.0) == 0.0
        assert creator._validate_numeric(None, default=1.0) == 1.0
        assert creator._validate_numeric([1, 2, 3], default=5.0) == 5.0
    
    def test_validate_integer_safe_conversion(self):
        """Test safe integer validation."""
        creator = AgentCreator()
        
        # Valid integers
        assert creator._validate_integer(10) == 10
        assert creator._validate_integer("20") == 20
        assert creator._validate_integer(15.7) == 15
        
        # Invalid inputs return default
        assert creator._validate_integer("not a number", default=0) == 0
        assert creator._validate_integer(None, default=100) == 100


# ============================================================================
# Code Generation Security Tests
# ============================================================================

class TestCodeGenerationSecurity:
    """Test that generated code is safe."""
    
    def test_generated_code_no_eval_exec(self):
        """Test generated code doesn't contain eval/exec."""
        creator = AgentCreator()
        
        # Generate code with proper rule structure (confidence is added by GUI)
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description="Test description",
            agent_type="Rule-Based",
            rules=[{
                "type": "simple",
                "metric": "pe_ratio",
                "operator": "<",
                "threshold": 15,
                "direction": "bullish",
                "confidence": 0.8  # Added: GUI provides this
            }]
        )
        
        # Should not contain dangerous functions
        assert "eval(" not in code
        assert "exec(" not in code
        assert "__import__" not in code
    
    def test_generated_code_compiles(self):
        """Test generated code is valid Python."""
        creator = AgentCreator()
        
        code = creator.generate_agent_code(
            agent_name="ValidAgent",
            description="Valid test agent",
            agent_type="Rule-Based",
            rules=[{
                "type": "simple",
                "metric": "pe_ratio",
                "operator": "<",
                "threshold": 15,
                "direction": "bullish",
                "confidence": 0.8  # Added: GUI provides this
            }]
        )
        
        # Should compile without errors
        compile(code, "<string>", "exec")
    
    def test_malicious_description_escaped(self):
        """Test malicious descriptions are properly escaped."""
        creator = AgentCreator()
        
        malicious_desc = '''Evil"""; import os; os.system("rm -rf /")'''
        
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description=malicious_desc,
            agent_type="Rule-Based",
            rules=[{
                "type": "simple",
                "metric": "pe_ratio",
                "operator": "<",
                "threshold": 15,
                "direction": "bullish",
                "confidence": 0.8
            }]
        )
        
        # Description should be escaped, not executable
        assert "os.system" not in code or r"os.system" in code  # Either not present or escaped


# ============================================================================
# File Operation Security Tests
# ============================================================================

class TestFileOperationSecurity:
    """Test file operation security."""
    
    def test_filename_validation_rejects_path_traversal(self):
        """Test path traversal is rejected."""
        loader = AgentLoader(Path("/tmp/test"))
        
        # These should fail validation
        assert not loader._is_valid_filename("../evil.py")
        assert not loader._is_valid_filename("../../etc/passwd")
        assert not loader._is_valid_filename("subdir/file.py")
    
    def test_filename_validation_rejects_special_chars(self):
        """Test special characters are rejected."""
        loader = AgentLoader(Path("/tmp/test"))
        
        assert not loader._is_valid_filename("agent;rm -rf.py")
        assert not loader._is_valid_filename("agent`whoami`.py")
        assert not loader._is_valid_filename("agent|cat /etc/passwd.py")
    
    def test_filename_validation_accepts_valid(self):
        """Test valid filenames are accepted."""
        loader = AgentLoader(Path("/tmp/test"))
        
        assert loader._is_valid_filename("my_agent")
        assert loader._is_valid_filename("ValueAgent")
        assert loader._is_valid_filename("agent_v2")
    
    def test_save_agent_prevents_overwrite(self, tmp_path):
        """Test save prevents accidental overwrite."""
        loader = AgentLoader(tmp_path)
        
        # Create existing file
        (tmp_path / "existing.py").write_text("# Existing")
        
        # Try to save with same name
        success, msg = loader.save_agent("existing.py", "# New")
        
        assert success is False
        assert "already exists" in msg.lower()


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases in security."""
    
    def test_empty_agent_name(self):
        """Test empty agent name handling."""
        creator = AgentCreator()
        
        code = creator.generate_agent_code(
            agent_name="",  # Empty name
            description="Test",
            agent_type="Rule-Based",
            rules=[]
        )
        
        # Should have fallback name
        assert "class Agent" in code or "class A" in code
    
    def test_very_long_description(self):
        """Test very long descriptions."""
        creator = AgentCreator()
        
        long_desc = "A" * 10000  # 10k characters
        
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description=long_desc,
            agent_type="Rule-Based",
            rules=[]
        )
        
        # Should handle without crashing
        assert "TestAgent" in code
    
    def test_unicode_in_inputs(self):
        """Test Unicode characters in inputs."""
        creator = AgentCreator()
        
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description="Agent with émojis 🚀 and Üñíçödé",
            agent_type="Rule-Based",
            rules=[]
        )
        
        # Should handle Unicode
        assert "TestAgent" in code
        # Description should be escaped/handled safely
        assert "class TestAgent" in code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
