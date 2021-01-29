from setuptools import setup

setup(name='carrier.usps',
      version='2020.11.1-beta',
      description='USPS Web API Schemas Python Data Types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.usps',
      author='Purplship Team',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['usps_lib'],
      install_requires=['six', 'lxml'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
