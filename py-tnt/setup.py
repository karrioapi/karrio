from setuptools import setup

setup(name='py-tnt',
      version='0.1.dev0',
      description='TNT Python Data Structure',
      url='https://github.com/OpenShip/py-tnt',
      author='DanH91',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pytnt'],
      exclude=["schemas"],
      zip_safe=False)