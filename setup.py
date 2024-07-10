import setuptools
import os 

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name='preflop_advisor',
    version='0.1',
    description='Reads Infos from exported Monker Trees for specific Hand',
    author='ksoeze',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required, 
    entry_points={
          'console_scripts': [
              'preflop_advisor = preflop_advisor.__main__:main'
          ],
          'gui_scripts': [
              'preflop_advisor = preflop_advisor.__main__:main'
          ]
      },
      )
