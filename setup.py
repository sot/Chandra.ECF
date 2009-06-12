import os

from setuptools import setup
setup(name='Chandra.ECF',
      author = 'Tom Aldcroft',
      description='Access the Chandra HRMA Enclosed Counts Fraction (ECF) data',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Chandra.ECF'],
      version='0.02',
      zip_safe=False,
      test_suite='nose.collector',
      namespace_packages=['Chandra'],
      packages=['Chandra'],
      package_dir={'Chandra' : 'Chandra'},
      package_data={'': ['*_ECF.fits']}
      )
