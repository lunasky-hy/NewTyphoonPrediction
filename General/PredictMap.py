import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import PearsonModel.Model
import EuclidModel.Model
from PearsonModel.Constant import Const

class PredictMap(object):
    """description of class"""
    def __init__(self, models):
        self.models = models   
        
    def show(self, init_pos):
        fig = plt.figure()
        
        X = np.arange(Const.PLOT_START_LONG, Const.PLOT_END_LONG + Const.PLOT_INTARVAL_LONG, Const.PLOT_INTARVAL_LONG)
        Y = np.arange(Const.PLOT_START_LAT, Const.PLOT_END_LAT + Const.PLOT_INTARVAL_LAT, Const.PLOT_INTARVAL_LAT)
        values = np.zeros([len(Y), len(X)])

        for lat in range(len(Y)):
            for long in range(len(X)):
                for model in self.models:
                    val = model.calcProbability(Y[lat], X[long])
                    if values[lat, long] == 0:
                        values[lat, long] = val

        m = Basemap(projection = 'merc',
                 resolution = 'l',
                 llcrnrlon = Const.PLOT_START_LONG,
                 llcrnrlat = Const.PLOT_START_LAT,
                 urcrnrlon = Const.PLOT_END_LONG,
                 urcrnrlat = Const.PLOT_END_LAT)
        m.drawcoastlines() 
        m.drawstates()
        
        m.imshow(values, cmap = 'Reds')
        # 5度ごとに緯度線を描く
        m.drawparallels(np.arange(Const.PLOT_START_LAT, Const.PLOT_END_LAT, 5), labels = [1, 0, 0, 0], fontsize=10)
        # 5度ごとに経度線を描く
        m.drawmeridians(np.arange(Const.PLOT_START_LONG, Const.PLOT_END_LONG, 5), labels = [0, 0, 0, 1], fontsize=10)

        oldx, oldy = m(init_pos[1], init_pos[0])
        for model in self.models:
            position = model.getPredictPosition()
            x, y = m(position[1], position[0])
            m.plot([oldx, x], [oldy, y])
            m.plot(x, y, 'x', markersize = 8)
            oldx = x
            oldy = y
        

        plt.title("Probability Field")
        plt.show()
