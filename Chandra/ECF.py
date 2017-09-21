# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Chandra.ECF is provides a simple method to access the Chandra HRMA Enclosed
Counts Fraction (ECF) data. 

http://cxc.harvard.edu/cal/Hrma/psf/
"""
import os
import pyfits
import numpy as np

__version__ = '0.2.1'

AXES = 'ECF THETA PHI ENERGY'.split()
ECFS = dict()

def interp_ECF(ecf=0.9, theta=0, phi=0, energy=1.5, shape='circular', value='radius'):
    """Compute a 4-d bilinear interpolation of the enclosed counts fraction
    radius provided by the CXC calibration group.

    :param ecf: Enclosed counts fraction (0 to 1)
    :param theta: Off-axis angle (arcmin)
    :param phi: Off-axis azimuth (deg)
    :param energy: Energy (keV)
    :param shape: 'circular' or 'elliptical'
    :param value: Column in the ECF file to interpolate (default=radius)

    :rtype: Interpolated ECF radius (arcsec)
    """
    if shape not in ECFS:
        ECFS[shape] = _read_ecf_file(shape)

    ECF = ECFS[shape]
    
    # Call interp1d to get two vectors corresponding to the indices and bilinear
    # interpolation of the axis values
    j, t = _interp1d(ECF['ecf'], ecf)
    k, u = _interp1d(ECF['theta'], theta)
    l, v = _interp1d(ECF['phi'], phi)
    m, w = _interp1d(ECF['energy'], energy)

    # The last element of phi is 360, which needs to wrap back to 0 for indexing into y
    l[1] = l[1] % (len(ECF['phi'])-1)

    # Do the actual 4-d bilinear interpolation on the desired ECF value using the
    # indexes and interpolants that were set up with interp1d
    y = ECF[value]
    yi = 0.0
    for dj in (0, 1):
        for dk in (0, 1):
            for dl in (0, 1):
                for dm in (0, 1):
                    yi += y[j[dj], k[dk], l[dl], m[dm]] * t[dj] * u[dk] * v[dl] * w[dm]

    return yi

def ECF_radius(radius=1.0, theta=0, phi=0, energy=1.5):
    """Determine the enclosed counts fraction for a given enclosed radius.

    :param radius: enclosed radius (arcsec)
    :param theta: Off-axis angle (arcmin)
    :param phi: Off-axis azimuth (deg)
    :param energy: Energy (keV)

    :rtype: Interpolated ECF (0 to 1)
    """
    # Brute force: calculate radii at ecf=0.01, 0.02, ... 0.99 and interpolate
    # Execution time ~ 20 msec => good enough.
    radii = [interp_ECF(i/100., theta, phi, energy) for i in range(1, 100)]
    if radius <= radii[0]:
        ecf = 0.01
    elif radius >= radii[-1]:
        ecf = 0.99
    else:
        irad = np.searchsorted(radii, [radius])[0]
        x = radius
        x0 = radii[irad-1]
        x1 = radii[irad]
        y0 = irad / 100.
        y1 = (irad+1) / 100.
        ecf = y0 + (y1-y0) / (x1-x0) * (x-x0)

    return ecf


def _read_ecf_file(shape):
    """Read the ECF data file (contained within package) and do some fixup.

    :param shape: 'circular' or 'elliptical'
    :rtype: dict of ECF file columns
    """
    filename = os.path.join(os.path.dirname(__file__), shape + '_ECF.fits')
    hdus = pyfits.open(filename)
    reef = hdus[1].data[0]              # Only one row
    colnames = hdus[1].data.dtype.names
    fields = 'RADIUS RADIUS_SMIN RADIUS_SMAX Y Z SMA SMB PA'.split()

    # Length of axis vectors.  This allows reshaping the corresponding
    # field array from a 1d vector to 4d array
    lens = [len(reef.field(x)) for x in AXES]
    ECF = dict((x.lower(), reef.field(x)) for x in AXES)
    for colname in set(fields) & set(colnames):
        ECF[colname.lower()] = reef.field(colname).reshape(lens, order='FORTRAN')

    # Put in a phantom entry for phi to ensure correct wrap in nearest
    # neighbor search (e.g. for phi=355)
    ECF['phi'] = np.append(ECF['phi'], np.float32(360.0))

    return ECF

def _interp1d(axis, x):
    """Bilinear interpolation of supplied ``axis``.  Returns (j, t) where
    ``j`` is a two-element list giving the indexes of the axis elements
    surrounding ``x``.  ``t`` is the bilinear interpolation of ``x`` between
    the surrounding axis elements (see code).

    :param axis: numpy array defining to grid points for this axis
    :rtype: (j, t)
    """
    try:
        j0 = np.where(axis <= x)[0][-1]
        j1 = j0 + 1
        a0 = axis[j0]
        a1 = axis[j1]
        t1 = (x - a0) / (a1 - a0)
        t0 = 1 - t1
    except IndexError:
        raise IndexError('Supplied x=%f not in range of axis (%f, %f)' % (x, axis[0], axis[-1]))

    return ([j0, j1], [t0, t1])

def _get_options():
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_defaults()
    parser.add_option("--ecf",
                      type='float',
                      default=0.9,
                      help="Enclosed counts fraction",
                      )
    parser.add_option("--theta",
                      type='float',
                      default=0,
                      help="Off-axis angle (arcmin)",
                      )
    parser.add_option("--phi",
                      type='float',
                      default=0,
                      help="Azimuthal angle (deg)",
                      )
    parser.add_option("--energy",
                      type='float',
                      default=1.5,
                      help="Energy (keV)",
                      )
    parser.add_option("--shape",
                      default='circular',
                      help="Shape (default=circular)",
                      )
    parser.add_option("--value",
                      default='radius',
                      help="Column in the ECF file to interpolate (default=radius)",
                      )
    (opt, args) = parser.parse_args()
    return (opt, args)


def _main():
    opt, args = _get_options()
    print interp_ECF(ecf=opt.ecf,
                     theta=opt.theta,
                     phi=opt.phi,
                     energy=opt.energy,
                     shape=opt.shape,
                     value=opt.value)

if __name__ == '__main__':
    _main()

