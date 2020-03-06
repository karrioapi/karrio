from setuptools import setup

setup(name='py-tnt',
      version='0.1.dev0',
      description='TNT Python Data Structure',
      url='https://github.com/OpenShip/py-tnt',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pytnt'],
      exclude=["schemas"],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False)