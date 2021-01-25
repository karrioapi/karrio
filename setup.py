from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("purplship/VERSION", "r") as v:
    version = v.read()

dev_requirements = [
      "bandit",
      "black",
      "coverage",
      "mypy",
      "click",
      "Jinja2",
      "mkdocs-material",
]

setup(name='purplship',
      version=version,
      description='Multi-carrier shipping API integration with python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship',
      author='Purplship Team',
      author_email='danielk.developer@gmail.com',
      license='LGPLv3',
      packages=find_packages(".", exclude=["tests*"]),
      install_requires=[
            'attrs',
            'jstruct',
            'xmltodict',
            'lxml',
            'lxml-stubs',
            'py-soap',
            'six',
            'Pillow',
            'phonenumbers'
      ],
      extras_require={
            'dev': dev_requirements
      },
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)
