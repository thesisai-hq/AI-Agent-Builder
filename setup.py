"""Setup configuration for AI Agent Framework."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-agent-framework",
    version="1.0.0",
    author="Jaee Oh",
    author_email="jaee@thesisai.app",
    description="Production-ready AI agent framework for financial analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thesisai-hq/AI-Agent-Builder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Framework :: Pytest",
        "Typing :: Typed",
    ],
    keywords="ai agent framework financial analysis llm rag postgresql fastapi",
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "asyncpg>=0.29.0",
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
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
        ],
        "all": [
            "openai>=1.3.0",
            "anthropic>=0.7.0",
            "ollama>=0.1.0",
            "sentence-transformers>=2.2.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-agent-framework/issues",
        "Source": "https://github.com/yourusername/ai-agent-framework",
        "Documentation": "https://github.com/yourusername/ai-agent-framework/tree/main/docs",
    },
)
