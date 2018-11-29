import numpy as np
import json
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import PearsonModel.StatisticTyphoon as typ
import PearsonModel.ProbabilityField as pf
from PearsonModel.Constant import Const

class AnalysisPredictErrorModel(object):
    # OK
    def __init__(self, position, file = "", init_time = 0):
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            exit()
            
        self.time = init_time
        self.position = position
        self.target_bandnum = []
        print("Loading")
        #if init_time == 0:
        #    self.__loadGPV__(file, Const.TARGET_BAND)
        print("Loading... Complete")

    def processing(self):
        print("Statistic Typhoon Loading...")
        self.__getStatisticTyphoon__()
        print("Statistic Typhoon Loading... Complete")
        print("Create Probability Field...")
        self.__getProbabilityField__()
        print('Finish Processing')
        
    def getPredictPosition(self):
        return self.field.getAverage()

    # 確率場の算出用
    def __getProbabilityField__(self):
        ave, var = self.__getMoveStat__()
        ave = [ave[0] + self.position[0], ave[1] + self.position[1]]
        self.field = pf.ProbabilityField(ave, var)

    # 過去台風のロード部分 - OK
    def __getStatisticTyphoon__(self):
        fp = open('./typhoon/TyphoonInfo.json', 'r')
        jsondata = json.load(fp)
        fp.close()
        self.statisticTyphoons = []
        del(jsondata['comment'])
        for index, info in jsondata.items():
            distance = self.GlobalDistance(self.position, [info['latitude'], info['longitude']])
            if distance > Const.STATISTIC_DISTANCE: # 中心が半径300kmの円の外側だったら飛ばす
                continue
            
            self.statisticTyphoons.append( typ.StatisticTyphoon(info, self.target_bandnum, flag = False) )
            print(str(len(self.statisticTyphoons)) + ':' + str(info['GPVfile']))

        print('Sample : ' + str(len(self.statisticTyphoons)))


    # 平均,分散の算出 - OK
    def __getMoveStat__(self):
        ave = [0.0, 0.0]
        var = [0.0, 0.0]
        for smodel in self.statisticTyphoons:
            move = smodel.getMovement()
            ave[0] += move[0]
            ave[1] += move[1]

        ave[0] = ave[0] / len(self.statisticTyphoons)
        ave[1] = ave[1] / len(self.statisticTyphoons)

        for smodel in self.statisticTyphoons:
            move = smodel.getMovement()
            var[0] += (move[0] - ave[0]) ** 2.0
            var[1] += (move[1] - ave[1]) ** 2.0

        var[0] = var[0] / len(self.statisticTyphoons)
        var[1] = var[1] / len(self.statisticTyphoons)

        return ave, var


    # GPV値のロード - OK
    def __loadGPV__(self, file, TARGET_BAND):
        
        fp = open(file, 'r')
        jsondata = json.load(fp)

        self.dataset = []
        for TARGET in TARGET_BAND:
            for datas in jsondata.values():
                if str(TARGET[0]) in datas['description'] and TARGET[1] in datas['metadata']['']['GRIB_COMMENT']:
                    info = { 
                        'Pressure' : datas['description'], 
                        'Element' : datas['metadata']['']['GRIB_COMMENT'], 
                        'Value' : self.__filtering__(np.array(datas['GPV']))}
                    self.target_bandnum.append(int(datas['band']))
                    self.dataset.append(info)
                    break
        fp.close()
    
    # 2点間の距離の算出 - OK
    def GlobalDistance(self, pos1, pos2):
        R = 6378.1370
        
        lat1 = math.radians(pos1[0])
        long1 = math.radians(pos1[1])
        lat2 = math.radians(pos2[0])
        long2 = math.radians(pos2[1])

        averageLat = (lat1 - lat2) / 2
        averageLong = (long1 - long2) / 2

        return R * 2 * math.asin( math.sqrt(math.pow( math.sin(averageLat), 2) + math.cos(lat1) * math.cos(lat2) * math.pow( math.sin(averageLong), 2)))

    # 角度の算出
    def AngularDifference(self, predict, real):
        Y = real[0] - predict[0]
        X = real[1] - predict[1]
        if X == 0.0:
            return np.pi / 2 if Y > 0 else - np.pi / 2
        return np.arctan2(Y, X)

    # フィルタリング - OK
    def __filtering__(self, datas):

        filtedValues = np.zeros([len(Const.CONVERTED_LATITUDE), len(Const.CONVERTED_LONGITUDE)])

        for latIndex, latValue in enumerate(Const.CONVERTED_LATITUDE):
            for longIndex, longValue in enumerate(Const.CONVERTED_LONGITUDE):

                original = self.__calcGPVIndexes__(latValue, longValue)
                filtedValues[latIndex, longIndex] = self.__Gaussian__(datas, original, Const.N)

        #self.__VisualFiltering__(datas, filtedValues)
        return filtedValues

    # 元データのインデックス番号を得る - OK
    def __calcGPVIndexes__(self, lat, long):
        latIndex = int(round((lat - 47.6) / (- 0.1)))
        longIndex = int(round((long - 120.0) / 0.125))
        return [latIndex, longIndex]

    # ガウシアンフィルタをかける - OK
    def __Gaussian__(self, datas, indexes, N):
        value = 0
        for y in np.arange(-N, N + 1, 1):
            for x in np.arange(-N, N + 1, 1):
                distance = np.sqrt(x ** 2 + y ** 2)
                K = 1.0 / (2.0 * 3.14) * np.exp(- distance / 2)

                # 領域範囲外の場合の処理
                yaxis = indexes[0] - y
                xaxis = indexes[1] - x
                if yaxis < 0:
                    yaxis = 0
                elif yaxis > 252:
                    yaxis = 252
                if xaxis < 0:
                    xaxis = 0
                elif xaxis > 240:
                    xaxis = 240
                value += K * datas[yaxis, xaxis]
        return value

    # フィルタを可視化する - OK
    def __VisualFiltering__(self, datas, fileted):
        
        fig = plt.figure()
        ax = fig.add_subplot(2, 1, 1, projection='3d')
        bx = fig.add_subplot(2, 1, 2, projection='3d')
        
        X1, Y1 = np.meshgrid(np.arange(120, 150.125, 0.125), np.arange(47.6, 22.3, -0.1))
        X2, Y2 = np.meshgrid(Const.CONVERTED_LONGITUDE,Const.CONVERTED_LATITUDE)

        ax.plot_surface(X1, Y1, datas, cmap='bwr')
        bx.plot_surface(X2, Y2, fileted, cmap='bwr')

        plt.show()