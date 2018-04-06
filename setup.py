from setuptools import setup

setup(name='open_mappers',
      version='0.1.dev0',
      description='Shipping providers gateways and mappers',
      url='https://github.com/OpenShip/open_mappers',
      author='DanH91',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['open_mappers'],
      install_requires=[
            'py-fedex==0.1.dev0',
            'py-dhl==0.1.dev0',
            'py-soap==0.1.dev0'
      ],
      dependency_links=[
            'git+https://github.com/OpenShip/py-fedex.git@master#egg=py-fedex-0.1.dev0',
            'git+https://github.com/OpenShip/py-dhl.git@master#egg=py-dhl-0.1.dev0',
            'git+https://github.com/OpenShip/py-soap.git@master#egg=py-soap-0.1.dev0'
      ],
      zip_safe=False)