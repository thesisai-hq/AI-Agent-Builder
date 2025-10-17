from setuptools import setup, find_packages

setup(
    name="agent_builder",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.8",  # ← Minimum version
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "psycopg2-binary>=2.9.9",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "rag": [
            "sentence-transformers>=2.2.2",
            "chromadb>=0.4.18",
        ],
        "performance": [
            "faiss-cpu>=1.7.4",
            "numpy>=1.24.3",
        ],
        "dev": [
            "pytest>=7.4.3",
            "black>=23.11.0",
        ],
    },
)
