from setuptools import setup, find_packages

setup(
    name="intelliagent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Intelligent Agent for Dynamic Decision Making",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/intelliagent",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
