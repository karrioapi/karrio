from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.server.core",
    version="2022.2.2",
    description="Multi-carrier shipping API Core module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purplship/purplship",
    author="purplship",
    author_email="hello@purplship.com",
    license="Apache License Version 2.0",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "purplship",
        "psycopg2-binary",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False,
    include_package_data=True,
)
