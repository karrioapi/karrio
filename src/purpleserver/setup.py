from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

dev_requirements = [
      'wheel',

      'purplship.canadapost',
      'purplship.dhl',
      'purplship.fedex',
      'purplship.package',
      'purplship.purolator',
      'purplship.ups',

      'eshipper.extension',
      'freightcom.extension',
]

setup(
      name='purplship-server',
      version='2020.8.0',
      description='Multi-carrier shipping API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship-server',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='AGPLv3',
      packages=find_packages("."),
      install_requires=[
            'django',
            'djangorestframework',
            'djangorestframework-camel-case',
            'drf-yasg',
            'purplship-server.core',
            'django-oauth-toolkit',
            'jsonfield',
            'python-decouple',
      ],
      entry_points={
            "console_scripts": ["purplship = purpleserver.__main__:main"]
      },
      extras_require={
            'dev': dev_requirements,
      },
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
      ],
      zip_safe=False,
      include_package_data=True
)
