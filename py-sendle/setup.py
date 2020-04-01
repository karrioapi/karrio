from setuptools import setup

setup(name='py-sendle',
      version='2020.4.0',
      description='Sendle Python Data domain library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-sendle',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pysendle'],
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