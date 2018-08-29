from setuptools import setup

setup(name='Preflop Advisor',
      version='0.1.0',
      packages=['preflop_advisor'],
      entry_points={
          'console_scripts': [
              'preflop_advisor = preflop_advisor.__main__:main'
          ],
          'gui_scripts': [
              'preflop_advisor = preflop_advisor.__main__:main'
          ]
      },
      )
