from setuptools import setup

setup(name='py-dicom',
      version='2020.11',
      description='Dicom API schemas Python Data types library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-dicom',
      author='Purplship Team',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pydicom'],
      install_requires=[
            'jstruct'
      ],
      dependency_links=[
            'https://git.io/purplship',
      ],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      zip_safe=False)