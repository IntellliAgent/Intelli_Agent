"""Setup script for IntelliAgent."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intelliagent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An intelligent agent for dynamic decision making",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/intelliagent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.2.0",
        "plotly>=5.0.0",
        "networkx>=2.5",
        "streamlit>=1.0.0",
        "scipy>=1.7.0",
        "psutil>=5.8.0",
        "memory_profiler>=0.60.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "pytest-benchmark>=3.4.1",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=3.9",
            "mypy>=0.910",
            "pre-commit>=2.15",
        ],
    },
)
