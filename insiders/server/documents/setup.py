from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio.server.documents",
    version="2022.3.1",
    description="Multi-carrier shipping API apps module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio",
    author="karrio",
    author_email="hello@karrio.io",
    license="Karrio Enterprise",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "weasyprint",
        "karrio.server.core",
        "karrio.server.orgs",
        "karrio.server.graph",
        "karrio.server.manager",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    include_package_data=True,
)
