from setuptools import setup

setup(name='carrier.boxknight',
      version='2020.11.1-beta',
      description='Boxknight API schemas Python Data types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.boxknight',
      author='Purplship Team',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['boxknight_lib'],
      install_requires=['jstruct'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
