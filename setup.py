# encoding: utf-8
from setuptools import setup

setup(name='synthetically',
      version='0.1',
      description='Speech synthesis utilities',
      url='https://github.com/gchrupala/synthetically',
      author='Grzegorz Chrupała',
      author_email='g.chrupala@uvt.nl',
      license='MIT',
      packages=['synthetically'],
      install_requires=['gtts','pydub'],
      zip_safe=False)
