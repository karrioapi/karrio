from setuptools import setup

setup(name='py-aups',
      version='1.0-alpha',
      description='Australia Post Python Data domain library',
      url='https://github.com/PurplShip/purplship-carriers/tree/master/py-aups',
      author='PurplShip',
      author_email='danielk.developer@gmail.com',
      license='MIT',
      packages=['pyaups'],
      install_requires=[
            'attrs==18.2.0',
            'jstruct==1.0.0'
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