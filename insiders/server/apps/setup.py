from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.server.apps",
    version="2022.2",
    description="Multi-carrier shipping API apps module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purplship/purplship",
    author="purplship",
    author_email="hello@purplship.com",
    license="Purplship Enterprise",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "purplship.server.iam",
        "purplship.server.core",
        "purplship.server.orgs",
        "purplship.server.graph",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    include_package_data=True,
)
