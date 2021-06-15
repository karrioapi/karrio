from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

dev_requirements = [
    "appdirs",
    "attrs",
    "black",
    "certifi",
    "chardet",
    "click",
    "coverage",
    "generateDS",
    "idna",
    "lxml",
    "requests",
    "six",
    "toml",
    "urllib3",
    "xmltodict",
    "mypy",
    "wheel",
]

setup(
    name="eshipper.extension",
    version="2021.6rc1",
    description="eShipper purplship extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Purplship/purplship-bridges/eshipper",
    license="LGPLv3",
    packages=find_namespace_packages(exclude=["tests*"]),
    install_requires=[
        "purplship>=2021.5",
        "purplship-server.core",
    ],
    extras_require={"dev": dev_requirements},
    dependency_links=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
