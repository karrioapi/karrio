from setuptools import setup

setup(name='py-boxknight',
      version='2020.10.0',
      description='Boxknight API schemas Python Data types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-boxknight',
      author='Purplship',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pyboxknight'],
      install_requires=[
            'jstruct'
      ],
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False)