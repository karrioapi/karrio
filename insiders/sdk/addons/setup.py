"""Warning: This setup.py is only there for git install until poetry support git subdirectory"""
from setuptools import setup, find_namespace_packages

setup(
    name="purplship.addons",
    version="0.0.0-dev",
    license="LGPLv3",
    packages=find_namespace_packages(exclude="tests*"),
    install_requires=[
        "purplship",
    ],
    zip_safe=False,
    include_package_data=True,
)
