from setuptools import setup

setup(name='py-purolator',
      version='2020.3.0',
      description='Purolator Python Data domain',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-purolator',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pypurolator'],
      exclude=["schemas"],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False)
