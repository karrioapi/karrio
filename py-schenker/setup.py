from setuptools import setup

setup(name='py-schenker',
      version='1.0-alpha',
      description='DB Shenker Services Python Data domain library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-schenker',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pyschenker'],
      exclude=["schemas"],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False)