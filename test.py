# Licensed under a 3-clause BSD style license - see LICENSE.rst
import nose.tools as nt

import Chandra.ECF
import numpy as np

def test_ecf_radius_plot():
    """Qualitatively compare ecf_radius.png with ecf_radius_POG.png"""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    thetas = range(0, 16)
    plt.figure(1, figsize=(5,5))
    for energy in (1.49, 6.4):
        for ecf in (0.5, 0.9):
            radavg = []
            for theta in thetas:
                rads = [Chandra.ECF.interp_ECF(ecf, theta, phi, energy) for phi in range(0, 360, 45)]
                radavg.append(sum(rads) / len(rads))
            plt.plot(thetas, radavg, '-')
    plt.xlim(0,15)
    plt.ylim(0,30)
    plt.savefig('ecf_radius.png')
    
def test_interp_ECF():
    nt.assert_almost_equal(Chandra.ECF.interp_ECF(0.5, 5, 45, 2.0), 1.8351397514)

def test_ECF_radius():
    nt.assert_almost_equal(Chandra.ECF.ECF_radius(1.8, 5, 45, 2.0), 0.4882049750)
