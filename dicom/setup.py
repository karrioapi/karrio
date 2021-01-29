from setuptools import setup

setup(name='carrier.dicom',
      version='2020.11.1-beta',
      description='Dicom Web API Schemas Python Data Types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/carrier.dicom',
      author='Purplship Team',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['dicom_lib'],
      install_requires=['jstruct'],
      classifiers=[
            "Framework :: Purplship",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
      ],
      zip_safe=False)
