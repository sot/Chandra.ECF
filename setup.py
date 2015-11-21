from setuptools import setup

from Chandra.ECF import __version__

setup(name='Chandra.ECF',
      author = 'Tom Aldcroft',
      description='Access the Chandra HRMA Enclosed Counts Fraction (ECF) data',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Chandra.ECF'],
      version=__version__,
      zip_safe=False,
      packages=['Chandra'],
      package_dir={'Chandra' : 'Chandra'},
      package_data={'': ['*_ECF.fits']}
      )
