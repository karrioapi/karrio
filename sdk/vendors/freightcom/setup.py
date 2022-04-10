"""Warning: This setup.py is only there for git install until poetry support git subdirectory"""

from setuptools import setup, find_namespace_packages

setup(
    name="karrio.freightcom",
    version="0.0.0-dev",
    license="Apache-2.0",
    packages=find_namespace_packages(exclude=["tests*"]),
    install_requires=["karrio"],
    zip_safe=False,
)
