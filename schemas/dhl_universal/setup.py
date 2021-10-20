"""Warning: This setup.py is only there for git install until poetry support git subdirectory"""

from setuptools import setup, find_packages

setup(
      name='carrier.dhl_universal',
      version='0.0.0-dev',
      license='MIT',
      packages=find_packages(),
      install_requires=['jstruct'],
      zip_safe=False,
)
