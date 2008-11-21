# from distutils.core import setup, Extension
import os

from setuptools import setup
setup(name='Chandra.ECF',
      author = 'Tom Aldcroft',
      description='Access the Chandra HRMA Enclosed Counts Fraction (ECF) data',
      author_email = 'taldcroft@cfa.harvard.edu',
      py_modules = ['Chandra.ECF'],
      version='1.0',
      zip_safe=False,
      namespace_packages=['Chandra'],
      packages=['Chandra'],
      package_dir={'Chandra' : 'Chandra'},
      package_data={'': ['*_ECF.fits']}
      )
