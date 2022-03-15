from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio.server.events",
    version="2022.2",
    description="Multi-carrier shipping API Events module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrio/karrio",
    author="karrio",
    author_email="hello@karrio.com",
    license="Apache License Version 2.0",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=["karrio.server.core", "huey"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False,
)
