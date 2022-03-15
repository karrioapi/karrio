from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio.server.iam",
    version="2022.4",
    description="Multi-carrier shipping API iam module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrio-inc/karrio",
    author="karrio",
    author_email="hello@karrio.io",
    license="Karrio Enterprise",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "django-oauth-toolkit",
        "karrio.server.core",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    include_package_data=True,
)
