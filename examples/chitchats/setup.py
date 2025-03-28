from setuptools import setup, find_namespace_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=f"karrio.chitchats",
    version="2024.3",
    author="Karrio Team",
    author_email="hello@karrio.io",
    description="Karrio Chit Chats carrier integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://karrio.io",
    project_urls={
        "Bug Tracker": "https://github.com/karrioapi/karrio/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(include=["karrio.*"]),
    python_requires=">=3.8",
    install_requires=[
        "karrio",
    ],
)
