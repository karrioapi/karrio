from setuptools import setup, find_namespace_packages


setup(
    name="purplship.ups_package",
    version="2021.0",
    description="Multi-carrier shipping API integration with python",
    url="https://github.com/PurplShip/purplship",
    author="Purplship Team",
    license="LGPLv3",
    packages=find_namespace_packages(),
    install_requires=[
        "purplship",
        "purplship.ups",
        "py-ups",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
