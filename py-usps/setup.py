from setuptools import setup

setup(name='py-usps',
      version='1.0-alpha',
      description='USPS Python Data Structure',
      url='https://github.com/OpenShip/py-usps',
      author='DanH91',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pyusps'],
      exclude=["schemas"],
      zip_safe=False)