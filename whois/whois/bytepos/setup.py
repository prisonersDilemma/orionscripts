#!/usr/bin/env python3.6

from setuptools import setup

setup(name='tail',
      description='"Walk" backwards through a file.',
      author='na',
      author_email='',
      license='Apache',
      keywords=['tail', 'bytes', 'walk',],
      url='https://github.com/prisonersDilemma/py3mods.git',
      version='0.1',
      packages=['../bytepos'],
      zipsafe=True,
      python_requires='>=3.5',
      #install_requires=[],
      #dependency_links=['file://../bytepos'],
      #dependency_links=['https://github.com/prisonersDilemma/py3mods.git'],
      #test_suite=,
      )

if __name__ == '__main__':
    pass
