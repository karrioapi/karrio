from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='purplship',
      version='2019.4.0',
      description='Multi-carrier shipping API integration with python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='Apache 2.0',
      packages=find_packages(".", exclude=["tests"]),
      install_requires=[
            'attrs',
            'jstruct',
            'py-fedex',
            'py-dhl',
            'py-soap',
            'gds-helpers',
            'py-ups',
            'py-caps',
            'py-aups',
            'py-sendle',
            'py-usps',
      ],
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
