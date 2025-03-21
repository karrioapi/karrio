from setuptools import setup, find_namespace_packages

# Read README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=f"karrio.plugin.test_plugin",
    version="0.1.0",
    author="Karrio Dev",
    author_email="author@example.com",
    description="A test plugin for Karrio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio",
    project_urls={
        "Documentation": "https://docs.karrio.io/",
        "Source": "https://github.com/karrioapi/karrio",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "karrio",
    ],
    python_requires=">=3.8",
)
