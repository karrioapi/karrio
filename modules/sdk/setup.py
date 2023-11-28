from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="karrio",
    version="2023.5.1",
    description="Multi-carrier shipping API integration with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/karrioapi/karrio",
    author="karrio",
    author_email="hello@karrio.io",
    license="Apache-2.0",
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=[
        "jstruct",
        "xmltodict",
        "lxml",
        "lxml-stubs",
        "py-soap",
        "Pillow",
        "phonenumbers",
        "python-barcode",
        "PyPDF2",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    include_package_data=True,
)
