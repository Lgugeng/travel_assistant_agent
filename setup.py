from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="travel-assistant-agent",
    version="1.0.0",
    author="Lgugeng",
    author_email="jacyl017l@gmail.com",
    description="基于 SiliconFlow 的智能旅行助手智能体",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lgugeng/travel-assistant-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "openai>=1.0.0",
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ]
    },
    keywords="ai agent travel assistant siliconflow llm",
)
