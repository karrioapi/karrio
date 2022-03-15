from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio.server.graph",
    version="2022.4",
    description="Multi-carrier shipping API Graph module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Karrio/karrio-server",
    author="karrio",
    author_email="hello@karrio.io",
    license="Apache License Version 2.0",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "karrio.server.core",
        "graphene-django",
        "django-filter",
    ],
    dependency_links=["https://git.io/karrio"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    zip_safe=False,
    include_package_data=True,
)
