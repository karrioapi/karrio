from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.server.pricing",
    version="2022.1.3",
    description="Multi-carrier shipping API Pricing panel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Purplship/purplship-server",
    author="purplship",
    author_email="hello@purplship.com",
    license="Apache License Version 2.0",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=["purplship.server.core"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False,
)
