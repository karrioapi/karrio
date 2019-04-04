from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='purplship',
      version='1.0.2',
      description='Multi-carrier shipping API integration with python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship',
      author='DanH91',
      author_email='danielk.developer@gmail.com',
      license='LGPLv3',
      packages=find_packages(".", exclude=["tests"]),
      install_requires=[
            'attrs==18.2.0',
            'jstruct==1.0.0',
            'py-fedex==1.1',
            'py-dhl==1.2',
            'py-soap==1.1',
            'gds-helpers==0.8.0',
            'py-ups==1.0',
            'py-caps==1.0',
            'py-aups==1.0a0',
            'py-sendle==1.0a0',
            'py-usps==1.0a0',
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
