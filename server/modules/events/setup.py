from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.server.events",
    version="2021.10rc1",
    description="Multi-carrier shipping API Events module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purplship/purplship",
    author="purplship",
    author_email="hello@purplship.com",
    license="Apache License Version 2.0",
    packages=find_namespace_packages("."),
    install_requires=["purplship.server.core", "huey"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False,
)
