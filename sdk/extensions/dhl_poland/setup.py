"""Warning: This setup.py is only there for git install until poetry support git subdirectory"""

from setuptools import setup, find_namespace_packages

setup(
    name="purplship.dhl_poland",
    version="0.0.0-dev",
    license="LGPLv3",
    packages=find_namespace_packages(),
    install_requires=["purplship", "carrier.dhl_poland"],
    zip_safe=False,
)
