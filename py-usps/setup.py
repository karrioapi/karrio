from setuptools import setup

setup(name='py-usps',
      version='2020.11',
      description='USPS Web API Schemas Python Datatypes library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-usps',
      author='Purplship Team',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pyusps'],
      exclude=["schemas"],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False)