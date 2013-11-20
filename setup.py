#!/usr/bin/env python

from os.path import join, dirname
from distutils.core import setup

packages = [
    'dsltool',
]

def get_version():
    g = {}
    execfile(join(dirname(__file__), 'src', 'dsltool', 'version.py'), g)
    return g['__version__']

setup(name='pydsltool',
      version=get_version(),
      description='A library to enable making simple domain specific languages',
      long_description=open(join(dirname(__file__), 'README'), 'r').read(),
      author='Dustin Spicuzza',
      author_email='dustin@virtualroadside.com',
      url='https://github.com/virtuald/pydsltool',
      license='Apache 2.0',
      packages=packages,
      package_dir={'': 'src'},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
      ]
)

