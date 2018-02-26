import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='typeform-python',
      version='0.1.1',
      description='API wrapper for Typeform written in Python',
      long_description=read('README.md'),
      url='https://github.com/GearPlug/typeform-python',
      author='Luisa Torres',
      author_email='hanna860@gmail.com',
      license='GPL',
      packages=['typeform'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
