import Chandra.ECF
import matplotlib.pyplot as plt
import numpy as np

def test_ecf_radius_plot():
    """Qualitatively compare plot with ecf_radius_POG.png"""
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
    
                    
    
    
