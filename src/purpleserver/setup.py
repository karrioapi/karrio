from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("purpleserver/VERSION", "r") as v:
    version = v.read()

dev_requirements = [
      'wheel',

      'purplship.canadapost',
      'purplship.dhl-express',
      'purplship.fedex',
      'purplship.fedex-express',
      'purplship.purolator',
      'purplship.purolator-courier',
      'purplship.ups',
      'purplship.ups-package',

      'eshipper.extension',
      'freightcom.extension',
]

setup(
      name='purplship-server',
      version=version,
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
            'django-email-verification',
            'djangorestframework==3.11.1',
            'drf-api-tracking',
            'drf-yasg',
            'gunicorn',
            'jsonfield',
            'more-itertools',
            'python-decouple',
            'purplship-server.core',
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
