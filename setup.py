from setuptools import setup, find_packages
import os
import re

# Lê a versão diretamente do arquivo version.py


def get_version():
    version_file = os.path.join(
        os.path.dirname(__file__),
        'intelliagent',
        'version.py'
    )
    with open(version_file, 'r', encoding='utf-8') as f:
        content = f.read()
        version_match = re.search(
            r'^__version__ = ["\']([^"\']*)["\']',
            content,
            re.M
        )
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


# Lê o README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="intelliagent",
    version=get_version(),
    author="Your Name",
    author_email="your.email@example.com",
    description="Intelligent Agent for Dynamic Decision Making",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/intelliagent",
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "sphinx>=7.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
        ],
    },
    package_data={
        "intelliagent": ["py.typed"],
    },
)
