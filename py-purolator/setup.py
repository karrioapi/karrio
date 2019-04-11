from setuptools import setup

setup(name='py-purolator',
      version='1.0-alpha',
      description='Purolator Python Data domain',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-purolator',
      author='DanH91',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pypurolator'],
      exclude=["schemas"],
      zip_safe=False)