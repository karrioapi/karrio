"""Warning: This setup.py is only there for git install until poetry support git subdirectory"""

from setuptools import setup, find_namespace_packages

setup(
      name='karrio.sf_express',
      version='0.0.0-dev',
      license='LGPLv3',
      packages=find_namespace_packages(),
      install_requires=['karrio', 'carrier.sf_express'],
      zip_safe=False,
)