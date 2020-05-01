from pathlib import Path
from setuptools import setup, find_packages

VERSION_FILE = str(Path(Path(__file__).resolve().parent, '../../VERSION.txt').resolve())

with open(VERSION_FILE, 'r') as f:
    version = f.readline()

setup(name='purplship.package',
      version=version,
      description='Multi-carrier shipping API integration with python',
      url='https://github.com/PurplShip/purplship',
      author='PurplShip',
      license='LGPLv3',
      packages=find_packages(".", exclude=["tests*"]),
      install_requires=[
            'purplship',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
