from setuptools import setup, find_namespace_packages

with open('../../VERSION.txt', 'r') as f:
    version = f.readline()

setup(name='purplship.ups',
      version=version,
      description='Multi-carrier shipping API integration with python',
      url='https://github.com/PurplShip/purplship',
      author='PurplShip',
      license='LGPLv3',
      packages=find_namespace_packages(exclude=["tests*"]),
      install_requires=[
            'purplship',
            'py-ups',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
