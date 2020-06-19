from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='purplship-server.extension',
    version='2020.6.1',
    description='Purplship-server extension',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PurplShip/purplship-extension',
    license='LGPLv3',
    packages=find_packages("."),
    install_requires=[
        'purplship-server.core>=2020.6.3',
    ],
    dependency_links=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
