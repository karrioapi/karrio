from setuptools import setup

setup(name='openship',
      version='1.0-beta.2',
      description='Shipping carriers mappers and proxies',
      url='https://github.com/OpenShip/openship',
      author='DanH91',
      author_email='danielk.developer@gmail.com',
      license='LGPL',
      packages=['openship'],
      install_requires=[
            'py-fedex==1.1',
            'py-dhl==1.1',
            'py-soap==1.1',
            'gds-helpers==0.3.0',
      ],
      dependency_links=[
            'git+https://github.com/OpenShip/py-fedex.git@v1.1#egg=py-fedex-1.1',
            'git+https://github.com/OpenShip/py-dhl.git@v1.1#egg=py-dhl-1.1',
            'git+https://github.com/OpenShip/py-soap.git@v1.1#egg=py-soap-1.1',
            'git+https://github.com/OpenShip/generateDs-helpers.git@v0.3.0#egg=gds-helpers-0.3.0',
      ],
      zip_safe=False)
