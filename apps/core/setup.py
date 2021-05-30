from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='purplship-server.core',
      version='2021.5',
      description='Multi-carrier shipping API Core module',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Purplship/purplship-server',
      author='Purplship',
      author_email='danielk.developer@gmail.com',
      license='Apache License Version 2.0',
      packages=find_namespace_packages(),
      install_requires=[
            'purplship',
            'psycopg2-binary',
      ],
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Apache Software License",
      ],
      zip_safe=False,
      include_package_data=True
)
