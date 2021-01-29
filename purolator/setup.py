from setuptools import setup

setup(name='carrier.purolator',
      version='2020.4.1',
      description='Purolator Web API Schemas Python Data Types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.purolator',
      author='Purplship',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['purolator_lib'],
      install_requires=['six', 'lxml'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
