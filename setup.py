import setuptools


setuptools.setup(
    name='preflop_advisor',
    version='0.1',
    description='Reads Infos from exported Monker Trees for specific Hand',
    author='ksoeze',
    packages=setuptools.find_packages(),
    include_package_data=True,
    
    entry_points={
          'console_scripts': [
              'preflop_advisor = preflop_advisor.__main__:main'
          ],
          'gui_scripts': [
              'preflop_advisor = preflop_advisor.__main__:main'
          ]
      },
      )
