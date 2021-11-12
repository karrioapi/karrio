from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.server.graph",
    version="2021.11",
    description="Multi-carrier shipping API Graph module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Purplship/purplship-server",
    author="purplship",
    author_email="hello@purplship.com",
    license="Apache License Version 2.0",
    packages=find_namespace_packages(),
    install_requires=[
        "purplship.server.core",
        "graphene-django",
        "django-filter",
    ],
    dependency_links=["https://git.io/purplship"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False,
)
