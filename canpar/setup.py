from setuptools import setup

setup(name='carrier.canpar',
      version='2020.10.1',
      description='Canpar Web API Schemas Python Data Types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.canpar',
      author='Purplship',
      author_email='hello@purplship.com',
      license='MIT',
      packages=['canpar_lib'],
      install_requires=['six', 'lxml'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
