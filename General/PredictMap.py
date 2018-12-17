import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import json
import collections as cl
import PearsonModel.InitialModel
import General.UpdateModel
import EuclidModel.Model
from General.Constant import Const

class PredictMap(object):
    """description of class"""
    def __init__(self, init_pos, models):
        self.models = models   
        self.init_pos = init_pos
        
    def show(self):
        fig = plt.figure()
        
        X = np.arange(Const.PLOT_START_LONG, Const.PLOT_END_LONG + Const.PLOT_INTARVAL_LONG, Const.PLOT_INTARVAL_LONG)
        Y = np.arange(Const.PLOT_START_LAT, Const.PLOT_END_LAT + Const.PLOT_INTARVAL_LAT, Const.PLOT_INTARVAL_LAT)
        values = np.zeros([len(Y), len(X)])

        max = [0, 0]
        for lat in range(len(Y)):
            for long in range(len(X)):
                for model in self.models:
                    val = model.calcProbability(Y[lat], X[long])
                    if values[lat, long] == 0:
                        values[lat, long] = val
                    if values[lat, long] > values[max[0], max[1]]:
                        max[0] = lat
                        max[1] = long

        temp = 0.0
        for long in range(len(X)):
            temp += values[max[0], long]# * Const.PLOT_INTARVAL_LAT * PLOT_INTARVAL_LONG

        print(temp)
        m = Basemap(projection = 'merc',
                 resolution = 'l',
                 llcrnrlon = Const.PLOT_START_LONG,
                 llcrnrlat = Const.PLOT_START_LAT,
                 urcrnrlon = Const.PLOT_END_LONG,
                 urcrnrlat = Const.PLOT_END_LAT)
        m.drawcoastlines() 
        m.drawstates()
        
        # 5度ごとに緯度線を描く
        m.drawparallels(np.arange(0, 90, 10), labels = [1, 0, 0, 0], fontsize=10)
        # 5度ごとに経度線を描く
        m.drawmeridians(np.arange(120, 150, 10), labels = [0, 0, 0, 1], fontsize=10)

        oldx, oldy = m(self.init_pos[1], self.init_pos[0])
        for model in self.models:
            position = model.getPredictPosition()
            x, y = m(position[1], position[0])
            m.plot([oldx, x], [oldy, y])
            m.plot(x, y, 'x', markersize = 6)
            oldx = x
            oldy = y
        tmpX, tmpY = np.meshgrid(X, Y)
        axesX, axesY = m(tmpX, tmpY)
        m.contourf(axesX, axesY, values, cmap = 'Reds', alpha = 0.5)
        

        plt.title("Probability Field")
        plt.show()

    def showOriginals(self, positionArray, colors):
        fig = plt.figure()
        
        X = np.arange(Const.PLOT_START_LONG, Const.PLOT_END_LONG + Const.PLOT_INTARVAL_LONG, Const.PLOT_INTARVAL_LONG)
        Y = np.arange(Const.PLOT_START_LAT, Const.PLOT_END_LAT + Const.PLOT_INTARVAL_LAT, Const.PLOT_INTARVAL_LAT)

        m = Basemap(projection = 'merc',
                 resolution = 'l',
                 llcrnrlon = Const.PLOT_START_LONG,
                 llcrnrlat = Const.PLOT_START_LAT,
                 urcrnrlon = Const.PLOT_END_LONG,
                 urcrnrlat = Const.PLOT_END_LAT)
        m.drawcoastlines() 
        m.drawstates()

        # 5度ごとに緯度線を描く
        m.drawparallels(np.arange(0, 90, 10), labels = [1, 0, 0, 0], fontsize=10)
        # 5度ごとに経度線を描く
        m.drawmeridians(np.arange(120, 150, 10), labels = [0, 0, 0, 1], fontsize=10)

        for index, pos in enumerate(positionArray):
            x, y = m(pos[1], pos[0])
            m.plot(x, y, 'x', markersize = 6, color = colors[index])
        
        plt.show()

    # 予測結果をＪＳＯＮでセーブ
    def save(self, filename):
        
        fw = open(filename + '.json', 'w')

        ys = cl.OrderedDict()

        ys['0h'] = {'latitude': self.init_pos[0], 'longitude': self.init_pos[1]}
        
        hour = 6
        for model in self.models:
            position = model.getPredictPosition()
            movement = model.getPredictMovement()
            data = cl.OrderedDict()
            data['latitude'] = position[0]
            data['longitude'] = position[1]
            data['move_lat'] = movement[0]
            data['move_long'] = movement[1]

            ys[str(hour) + 'h'] = data
            hour += 6
        json.dump(ys, fw, indent = 4)
        del(ys)
        fw.close()