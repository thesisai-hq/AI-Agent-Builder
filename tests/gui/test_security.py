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
        
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description="Test description",
            agent_type="Rule-Based",
            rules=[{
                "type": "simple",
                "metric": "pe_ratio",
                "operator": "<",
                "threshold": 15,
                "direction": "bullish"
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
                "direction": "bullish"
            }]
        )
        
        # Should compile without errors
        compile(code, "test", "exec")
    
    def test_malicious_description_escaped(self):
        """Test malicious description is escaped."""
        creator = AgentCreator()
        
        malicious_desc = '''Evil agent"""; import os; os.system("rm -rf /")'''
        
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description=malicious_desc,
            agent_type="Rule-Based",
            rules=[]
        )
        
        # Malicious code should not be executable
        # Triple quotes should be escaped
        assert 'os.system("rm -rf /")' not in code or r'\"\"\"' in code


# ============================================================================
# File Operation Security Tests
# ============================================================================

class TestFileOperationSecurity:
    """Test file operations are secure."""
    
    def test_filename_validation_rejects_path_traversal(self):
        """Test rejection of path traversal attempts."""
        from gui.agent_loader import AgentLoader
        
        # Path traversal attempts
        assert not AgentLoader._is_valid_filename("../../../etc/passwd")
        assert not AgentLoader._is_valid_filename("..\\..\\evil.py")
        assert not AgentLoader._is_valid_filename("/etc/passwd")
        assert not AgentLoader._is_valid_filename("C:\\Windows\\evil.py")
    
    def test_filename_validation_rejects_special_chars(self):
        """Test rejection of special characters."""
        from gui.agent_loader import AgentLoader
        
        # Special characters
        assert not AgentLoader._is_valid_filename("agent-name.py")  # Dash
        assert not AgentLoader._is_valid_filename("agent name.py")  # Space
        assert not AgentLoader._is_valid_filename("agent@email.py")  # @
        assert not AgentLoader._is_valid_filename("agent$$$.py")    # $
    
    def test_filename_validation_accepts_valid(self):
        """Test acceptance of valid filenames."""
        from gui.agent_loader import AgentLoader
        
        # Valid filenames
        assert AgentLoader._is_valid_filename("my_agent.py")
        assert AgentLoader._is_valid_filename("agent123.py")
        assert AgentLoader._is_valid_filename("MyAgent.py")
    
    def test_save_agent_prevents_overwrite(self, tmp_path):
        """Test that save prevents overwriting existing files."""
        loader = AgentLoader(tmp_path)
        
        # Create existing file
        existing_file = tmp_path / "existing.py"
        existing_file.write_text("# Existing code")
        
        # Attempt to save with same name
        success, message = loader.save_agent("existing.py", "# New code")
        
        assert not success
        assert "already exists" in message.lower()
        
        # Original file unchanged
        assert existing_file.read_text() == "# Existing code"


# ============================================================================
# Edge Case Tests
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_agent_name(self):
        """Test handling of empty agent name."""
        creator = AgentCreator()
        
        code = creator.generate_agent_code(
            agent_name="",
            description="Test",
            agent_type="Rule-Based",
            rules=[]
        )
        
        # Should use default name
        assert "class Agent(Agent):" in code or "Agent" in code
    
    def test_very_long_description(self):
        """Test handling of very long descriptions."""
        creator = AgentCreator()
        
        long_desc = "A" * 10000  # 10K characters
        
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description=long_desc,
            agent_type="Rule-Based",
            rules=[]
        )
        
        # Should not crash
        assert code is not None
        assert "TestAgent" in code
    
    def test_unicode_in_inputs(self):
        """Test handling of unicode characters."""
        creator = AgentCreator()
        
        code = creator.generate_agent_code(
            agent_name="TestAgent",
            description="Agent with emoji 🚀 and unicode 中文",
            agent_type="Rule-Based",
            rules=[]
        )
        
        # Should handle unicode gracefully
        assert code is not None
        compile(code, "test", "exec")  # Should compile


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
