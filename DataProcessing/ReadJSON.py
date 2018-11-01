import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def read(file):
    fp = open(file, 'r')
    jsondata = json.load(fp)

    bandnum = 3

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    
    band_meta = jsondata[str(bandnum)]['metadata']['']
    X1, Y1 = np.meshgrid(np.arange(120, 150.125, 0.125), np.arange(47.6, 22.3, -0.1))
    array2d = np.array(jsondata[str(bandnum)]['GPV'])
    ax.plot_surface(X1, Y1, array2d, cmap='bwr')
    ax.set_title(band_meta['GRIB_COMMENT'])

    plt.show()