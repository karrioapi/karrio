from setuptools import setup

setup(name='carrier.fedex',
      version='2020.3.1',
      description='Fedex Web API Schemas Python Data Types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.fedex',
      author='Purplship',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['fedex_lib'],
      install_requires=['six', 'lxml'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
