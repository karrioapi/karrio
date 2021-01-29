from setuptools import setup

setup(name='carrier.dhl_express',
      version='2020.4.1',
      description='DHL Web API Schemas Python Data Types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.dhl',
      author='Purplship',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['dhl_express_lib'],
      install_requires=['six', 'lxml'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
