"""Enhanced code viewer with educational annotations for learning.

This module displays agent code in a learning-friendly way, breaking it down
into sections with explanations to help finance students understand Python.
"""

import re

import streamlit as st


class CodeViewer:
    """Display agent code with helpful annotations for learning."""

    @staticmethod
    def show_with_annotations(code: str, filename: str):
        """Display code with educational annotations.

        Args:
            code: Python code to display
            filename: Agent filename
        """
        st.title(f"👁️ Learning from: {filename}")

        # Back button
        if st.button("← Back to Browse", type="primary"):
            st.session_state.current_viewing_file = None
            st.rerun()

        # Educational tips at top
        st.info("""
        💡 **How to Learn from This Code:**

        1. **Read the comments** - Lines starting with `#` explain what the code does
        2. **Notice the structure** - Imports → Class definition → Methods → Main function
        3. **Focus on `analyze()` method** - This is where the investment logic happens
        4. **Try modifying values** - Download the code, change numbers, see what happens!
        5. **Don't worry if you don't understand everything** - You'll learn gradually

        **Remember:** This code was auto-generated. You can create agents without knowing Python!
        """)

        st.markdown("---")

        # Parse and display code sections
        sections = CodeViewer._parse_code_sections(code, filename)

        st.markdown("### 📖 Code Breakdown (Learning Mode)")

        for section in sections:
            with st.expander(f"**{section['title']}**", expanded=section.get("important", False)):
                st.markdown(f"**What this does:** {section['explanation']}")
                st.code(section["code"], language="python", line_numbers=False)

                if section.get("learning_note"):
                    st.caption(f"💡 **Learning Tip:** {section['learning_note']}")

        st.markdown("---")

        # Full code view
        st.markdown("### 📜 Complete Code")
        st.caption("This is the full code all together. You can copy or download it below.")
        st.code(code, language="python", line_numbers=True)

        st.markdown("---")

        # Action buttons
        st.markdown("### 💾 Actions")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "⬇️ Download Code",
                data=code,
                file_name=filename,
                mime="text/x-python",
                use_container_width=True,
                help="Download this code to your computer",
            )

        with col2:
            if st.button(
                "📋 Show Path", use_container_width=True, help="Show where this file is saved"
            ):
                st.code(f"examples/{filename}", language="bash")

        with col3:
            if st.button("← Back to Browse", use_container_width=True):
                st.session_state.current_viewing_file = None
                st.rerun()

        # Learning resources footer
        st.markdown("---")
        st.info(
            """
        ### 🎓 Next Steps for Learning

        **To understand this code better:**
        1. Download it and open in a text editor
        2. Try running it: `python examples/{filename}`
        3. Modify one number and run again - see what changes
        4. Compare with other agent files
        5. Read Python basics: https://docs.python.org/3/tutorial/

        **To use this agent:**
        1. Go to "🧪 Test Agent" tab
        2. Select this agent
        3. Run it with test data
        4. See how your code executes!

        **Remember:** You don't need to understand all the code to use agents.
        The GUI creates working code for you! Learning Python is optional but helpful.
        """.format(filename=filename)
        )

    @staticmethod
    def _parse_code_sections(code: str, filename: str) -> list:
        """Parse code into logical sections for learning.

        Args:
            code: Python code string
            filename: Agent filename

        Returns:
            List of section dictionaries with code and explanations
        """
        sections = []

        # Section 1: Imports
        imports = []
        for line in code.split("\n"):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                imports.append(line)

        if imports:
            sections.append(
                {
                    "title": "1. Imports - Getting the Tools We Need",
                    "explanation": (
                        "These lines import the building blocks we need to create our agent. "
                        "Think of it like gathering tools before starting a project. "
                        "We import Agent (base class), Signal (return type), Database (data access), etc."
                    ),
                    "code": "\n".join(imports),
                    "learning_note": (
                        'In Python, `import` means "use code from another file". '
                        "We're using pre-built tools from the agent_framework."
                    ),
                    "important": False,
                }
            )

        # Section 2: Class definition
        class_match = re.search(r"class\s+(\w+)\(Agent\):", code)
        if class_match:
            class_name = class_match.group(1)

            # Extract docstring
            docstring_match = re.search(r'class.*?"""(.*?)"""', code, re.DOTALL)
            docstring = docstring_match.group(1).strip() if docstring_match else "Investment agent"

            # Get just the class line and docstring
            class_def_match = re.search(r'(class\s+\w+\(Agent\):.*?""".*?""")', code, re.DOTALL)

            if class_def_match:
                class_code = class_def_match.group(1)
            else:
                class_code = class_match.group(0)

            # Truncate docstring if too long to avoid overflow
            docstring_preview = docstring[:150] if len(docstring) > 150 else docstring
            if len(docstring) > 150:
                docstring_preview += "..."

            sections.append(
                {
                    "title": f'2. Agent Definition - "{class_name}" Class',
                    "explanation": (
                        f'This defines our agent class called "{class_name}". '
                        f"A class is like a blueprint or template. {docstring_preview} "
                        'This agent inherits from "Agent" which means it gets all the base functionality.'
                    ),
                    "code": class_code,
                    "learning_note": (
                        "Think of a class like a cookie cutter - it defines the shape. "
                        "When we use this class later (create an instance), we get an actual agent object."
                    ),
                    "important": True,
                }
            )

        # Section 3: __init__ method (if present)
        init_match = re.search(
            r"    def __init__\(self.*?\):.*?(?=\n    async def|\n    def |\nclass|\nasync def main)",
            code,
            re.DOTALL,
        )

        if init_match:
            sections.append(
                {
                    "title": "3. Configuration - Setting Up the Agent",
                    "explanation": (
                        "The __init__ method runs when you create an agent. "
                        "It sets up the agent's configuration like which AI model to use, "
                        "what temperature setting, and any other settings. "
                        'This is like configuring the agent\'s "personality" and "tools".'
                    ),
                    "code": init_match.group(0),
                    "learning_note": (
                        "__init__ is a special Python method that runs automatically when you create an object. "
                        '"self" refers to the agent instance itself.'
                    ),
                    "important": True,
                }
            )

        # Section 4: analyze() method - THE KEY METHOD
        # Stop at double newline before top-level definitions (main, class, etc.)
        analyze_match = re.search(
            r"(    async def analyze\(.*?\):.*?)(?=\n\n(?:async def|def|class)|\Z)",
            code,
            re.DOTALL,
        )

        if analyze_match:
            sections.append(
                {
                    "title": "4. Analysis Logic - The Brain 🧠 (MOST IMPORTANT)",
                    "explanation": (
                        "This is THE most important part! The analyze() method is where decisions happen. "
                        "It receives stock data, applies your strategy (rules or AI), and returns a Signal. "
                        "Everything else in the code supports this one method."
                    ),
                    "code": analyze_match.group(0),
                    "learning_note": (
                        "Focus on understanding THIS method. "
                        "For rule-based: Look for if/else statements checking values. "
                        "For LLM: Look for self.llm.chat() calling the AI. "
                        "For RAG: Look for self.rag.query() searching documents."
                    ),
                    "important": True,
                }
            )

        # Section 5: Private helper methods (if any, excluding __init__)
        # Find methods starting with single _ (not __ dunder methods)
        helper_pattern = r"    def (_[^_]\w*)\(self"
        helper_methods = re.findall(helper_pattern, code)
        
        if helper_methods:
            sections.append(
                {
                    "title": "5. Helper Methods - Supporting Functions",
                    "explanation": (
                        f"These are private helper methods (start with _) that support the main analyze() method. "
                        f"They break complex logic into smaller, manageable pieces. "
                        f"Found {len(helper_methods)} helper method(s)."
                    ),
                    "code": "# Helper methods found: " + ", ".join([m for m in helper_methods]),
                    "learning_note": (
                        'Methods starting with _ are "private" - they\'re internal helpers '
                        "not meant to be called from outside the class."
                    ),
                    "important": False,
                }
            )

        # Section 6: Main function
        main_match = re.search(r"(async def main\(\):.*?)(?=\n\nif __name__|$)", code, re.DOTALL)

        if main_match:
            # Truncate if too long
            main_code = main_match.group(1)
            if len(main_code) > 800:
                main_code = main_code[:800] + "\n    # ... (truncated for readability)"

            sections.append(
                {
                    "title": "6. Example Usage - How to Run It",
                    "explanation": (
                        "The main() function shows how to use the agent. "
                        "It connects to the database, creates the agent, gets data, "
                        "and runs analysis. This is example code to help you understand usage."
                    ),
                    "code": main_code,
                    "learning_note": (
                        f"To run this agent: python examples/{filename}\n"
                        "The main() function is like a demo/test of the agent."
                    ),
                    "important": False,
                }
            )

        # Section 7: Entry point
        if '__name__ == "__main__"' in code:
            sections.append(
                {
                    "title": "7. Entry Point - Starting the Program",
                    "explanation": (
                        "This line makes the file runnable as a script. "
                        'When you run "python examples/file.py", this section executes '
                        'and calls the main() function. It\'s like the "start button" of the program.'
                    ),
                    "code": 'if __name__ == "__main__":\n    asyncio.run(main())',
                    "learning_note": (
                        'This is Python boilerplate. It means "if this file is run directly '
                        "(not imported), then execute main()\". You'll see this in most Python scripts."
                    ),
                    "important": False,
                }
            )

        return sections


def show_simple_code_view(code: str, filename: str):
    """Simple code viewer without annotations (fallback).

    Args:
        code: Python code string
        filename: Agent filename
    """
    st.title(f"👁️ Viewing: {filename}")

    # Back button
    if st.button("← Back to Browse", type="primary"):
        st.session_state.current_viewing_file = None
        st.rerun()

    st.markdown("---")

    # Educational note
    st.info("""
    💡 **Reading This Code:**
    - Lines with `#` are comments explaining the code
    - `class` defines the agent template
    - `def analyze` is where decisions happen
    - `return Signal(...)` is what the agent outputs

    **Don't worry if some parts look confusing** - focus on the overall structure!
    """)

    # Display code with line numbers
    st.code(code, language="python", line_numbers=True)

    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            "⬇️ Download Code",
            data=code,
            file_name=filename,
            mime="text/x-python",
            use_container_width=True,
        )

    with col2:
        if st.button("📋 Copy Path", use_container_width=True):
            st.code(f"examples/{filename}", language="bash")

    with col3:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_viewing_file = None
            st.rerun()


# Main entry point
if __name__ == "__main__":
    # Test the code viewer
    sample_code = """
import asyncio
from agent_framework import Agent, Signal

class TestAgent(Agent):
    \"\"\"Simple test agent.\"\"\"

    async def analyze(self, ticker: str, data: dict) -> Signal:
        pe = data.get('pe_ratio', 0)

        if pe < 15:
            return Signal('bullish', 0.8, 'Undervalued')
        return Signal('neutral', 0.5, 'Fair')

async def main():
    agent = TestAgent()
    signal = agent.analyze('AAPL', {'pe_ratio': 12})
    print(signal)

if __name__ == "__main__":
    asyncio.run(main())
"""

    CodeViewer.show_with_annotations(sample_code, "test_agent.py")
