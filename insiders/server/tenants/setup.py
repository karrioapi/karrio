from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="purplship.server.tenants",
    version="2021.11",
    description="Multi-carrier shipping API muti-tenant module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/purplship/purplship",
    author="purplship",
    author_email="hello@purplship.com",
    license="Purplship Enterprise",
    packages=find_namespace_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "purplship.server.core",
        "django-tenants",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
)
