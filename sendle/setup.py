from setuptools import setup

setup(name='carrier.sendle',
      version='2020.4.1',
      description='Sendly API Schemas Python Data Types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.sendle',
      author='Purplship',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['sendle_lib'],
      install_requires=['jstruct'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
