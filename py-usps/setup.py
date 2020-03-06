from setuptools import setup

setup(name='py-usps',
      version='1.0-alpha',
      description='USPS Python Data Structure',
      url='https://github.com/OpenShip/py-usps',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pyusps'],
      exclude=["schemas"],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False)