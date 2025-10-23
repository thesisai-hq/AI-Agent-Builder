"""Setup configuration for AI Agent Framework."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-agent-framework",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Simple, maintainable AI agent builder framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-agent-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "llm": [
            "openai>=1.3.0",
            "anthropic>=0.7.0",
            "ollama>=0.1.0",
        ],
        "rag": [
            "sentence-transformers>=2.2.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.11.0",
        ],
        "all": [
            "openai>=1.3.0",
            "anthropic>=0.7.0",
            "ollama>=0.1.0",
            "sentence-transformers>=2.2.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.11.0",
        ],
    },
)