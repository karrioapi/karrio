from setuptools import setup, find_namespace_packages


setup(
    name="purplship.purolator",
    version="2020.12",
    description="Multi-carrier shipping API integration with python",
    url="https://github.com/PurplShip/purplship",
    author="Purplship Team",
    license="LGPLv3",
    packages=find_namespace_packages(),
    install_requires=[
        "py-purolator",
        "purplship",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
