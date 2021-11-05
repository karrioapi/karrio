"""Warning: This setup.py is only there for git install until poetry support git subdirectory"""

from setuptools import setup, find_namespace_packages

setup(
      name='purplship.ics_courier',
      version='0.0.0-dev',
      license='LGPLv3',
      packages=find_namespace_packages(),
      install_requires=['purplship', 'carrier.ics_courier'],
      zip_safe=False,
)