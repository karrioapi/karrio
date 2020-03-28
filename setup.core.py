from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='purplship.core',
      version='2020.3.0-beta1',
      description='Multi-carrier shipping API integration with python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='LGPLv3',
      packages=find_packages(
            ".",
            exclude=["*mappers.*"],
            include=[
                  "purplship",
                  "purplship.core*",
                  "purplship.freight*",
                  "purplship.package*",
                  "purplship.extension*"
            ]
      ),
      install_requires=[
            'attrs',
            'jstruct',
            'xmltodict',
            'lxml',
            'py-soap',
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
