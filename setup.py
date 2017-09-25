from setuptools import setup

setup(name='typeform',
      version='0.1',
      description='API wrapper for Typeform written in Python',
      url='https://github.com/GearPlug/typeform-python',
      author='Luisa Torres',
      author_email='hanna860@gmail.com',
      license='GPL',
      packages=['typeform'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
