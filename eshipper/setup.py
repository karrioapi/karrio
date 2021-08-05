from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.eshipper",
    version="2021.7",
    description="eShipper purplship extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purplship/purplship-bridges/eshipper",
    license="LGPLv3",
    packages=find_namespace_packages(exclude=["tests*"]),
    install_requires=[
        "django",
        "purplship>=2021.7",
        "purplship-server.core",
    ],
    dependency_links=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
