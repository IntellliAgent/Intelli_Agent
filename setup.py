"""Setup configuration for IntelliAgent package."""

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

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements/base.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip()
                    and not line.startswith("#")]

setup(
    name="intelliagent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A sophisticated AI agent framework",
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
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=0.9",
            "flake8>=3.9",
        ],
    },
    entry_points={
        "console_scripts": [
            "intelliagent=intelliagent.cli:main",
        ],
    },
)
