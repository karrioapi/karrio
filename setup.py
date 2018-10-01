from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='purplship',
      version='1.0-beta.6',
      description='Shipping carriers integration with python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/PurplShip/purplship',
      author='DanH91',
      author_email='danielk.developer@gmail.com',
      license='LGPL',
      packages=['purplship'],
      install_requires=[
            'py-fedex==1.1',
            'py-dhl==1.2',
            'py-soap==1.1',
            'gds-helpers==0.4.0',
            'py-ups==1.0',
            'py-caps==1.0',
      ],
      dependency_links=[
            'git+https://github.com/PurplShip/py-fedex.git@v1.1#egg=py-fedex-1.1',
            'git+https://github.com/PurplShip/py-dhl.git@v1.2#egg=py-dhl-1.2',
            'git+https://github.com/PurplShip/py-soap.git@v1.1#egg=py-soap-1.1',
            'git+https://github.com/PurplShip/generateDs-helpers.git@v0.4.0#egg=gds-helpers-0.4.0',
            'git+https://github.com/PurplShip/py-ups.git@v1.0#egg=py-ups-1.0',
            'git+https://github.com/PurplShip/py-caps.git@v1.0#egg=py-caps-1.0',
      ],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
      ],
      zip_safe=False)
