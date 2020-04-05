from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='freightcom.extension',
    version='2020.4.0',
    description='Freightcom purplship extension',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PurplShip/purplship-freightcom-extension',
    license='LGPLv3',
    packages=find_packages(".", exclude=["tests*"]),
    install_requires=[
        'six',
        'purplship.package'
    ],
    dependency_links=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
