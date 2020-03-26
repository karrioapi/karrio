from setuptools import setup, find_packages

with open("builds/package/README.md", "r") as fh:
    long_description = fh.read()


setup(name='purplship.freight',
      version='2020.3.0',
      description='Multi-carrier freight Library',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='LGPLv3',
      packages=find_packages(".", exclude=["purplship.package*", "tests*"]),
      install_requires=[
            'attrs',
            'jstruct',
            'xmltodict',
            'lxml',
            'py-fedex',
            'py-dhl',
            'py-soap',
            'py-ups',
      ],
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
