from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='purplship-server.graph',
      version='2021.3',
      description='Multi-carrier shipping API Graph module',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship-server',
      author='Purplship',
      author_email='danielk.developer@gmail.com',
      license='AGPLv3',
      packages=find_namespace_packages(),
      install_requires=[
            'purplship-server.core',
            'graphene-django',
      ],
      dependency_links=['https://git.io/purplship'],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
      ],
      zip_safe=False
)
