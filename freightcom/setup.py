from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.freightcom",
    version="2021.8",
    description="Freightcom purplship extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purplship/purplship-bridges/freightcom",
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
