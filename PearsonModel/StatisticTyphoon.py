import json
import numpy as np
from PearsonModel.Constant import Const

class StatisticTyphoon(object):
    """description of class"""
    def __init__(self, typhoon_dict, TARGET_BAND_NUM):
        self.file = self.__getGPVfromFile__(typhoon_dict['GPVfile'], TARGET_BAND_NUM)
        self.position = [typhoon_dict['latitude'], typhoon_dict['longitude']] 
        self.movement = typhoon_dict['movement']
        self.analogies = np.zeros(len(Const.TARGET_BAND))

    def getMovement(self):
        return self.movement

    # 類似度の計算 - OK
    def calcAnalogy(self, data, bandIndex, INDEXES):
        Xave = 0
        Yave = 0
        Sxy = 0
        Sx = 0
        Sy = 0

        for index in INDEXES:
            Xave += self.dataset[bandIndex]['Values'][ index[0], index[1] ]
            Yave += data[bandIndex]['Value'][ index[0], index[1] ]

        Xave = Xave / len(INDEXES)
        Yave = Yave / len(INDEXES)

        for index in INDEXES:
            Sxy += (self.dataset[bandIndex]['Values'][ index[0], index[1] ] - Xave) * (data[bandIndex]['Value'][ index[0], index[1] ] - Yave)
            Sx += (self.dataset[bandIndex]['Values'][ index[0], index[1] ] - Xave) ** 2
            Sy += (data[bandIndex]['Value'][ index[0], index[1] ] - Yave) ** 2

        self.analogies[bandIndex] = Sxy / (np.sqrt(Sx) * np.sqrt(Sy))

    # 類似度の平均の算出 - OK
    def aveAnalogy(self):
        self.analogy = np.average(self.analogies)
        return self.analogy

    def getAveAnalogy(self):
        return self.analogy

    # GPVを取得 - OK
    def __getGPVfromFile__(self, fname, TARGET_BAND_NUM):
        
        fp = open(fname, 'r')
        jsondata = json.load(fp)

        self.dataset = []
        for TARGET in TARGET_BAND_NUM:
            for datas in jsondata.values():
                if datas['band'] == TARGET:
                    info = { 'Pressure' : datas['description'], 'Element' : datas['metadata']['']['GRIB_COMMENT'], 'Values' : self.filtering(np.array(datas['GPV']))}
                    self.dataset.append(info)
                    break
        fp.close()

    # 格子間隔のフィルタリング - OK
    def filtering(self, dataset):

        filtedValues = np.zeros([len(Const.CONVERTED_LATITUDE), len(Const.CONVERTED_LONGITUDE)])

        for latIndex, latValue in enumerate(Const.CONVERTED_LATITUDE):
            for longIndex, longValue in enumerate(Const.CONVERTED_LONGITUDE):

                original = self.__calcGPVIndexes__(latValue, longValue)
                filtedValues[latIndex, longIndex] = self.__Gaussian__(dataset, original, Const.N)

        return filtedValues

    # 元データのインデックス番号を得る - OK
    def __calcGPVIndexes__(self, lat, long):
        latIndex = int(round((lat - 47.6) / (- 0.1)))
        longIndex = int(round((long - 120.0) / 0.125))
        return [latIndex, longIndex]

    # ガウシアンフィルタをかける - OK
    def __Gaussian__(self, dataset, indexes, N):
        value = 0
        for y in np.arange(-N, N + 1, 1):
            for x in np.arange(-N, N + 1, 1):
                distance = np.sqrt(x ** 2 + y ** 2)
                K = 1.0 / (2.0 * 3.14) * np.exp(- distance / 2)

                # 領域範囲外の場合の処理
                yaxis = indexes[0] - y
                xaxis = indexes[1] - x
                if yaxis < 0 : yaxis = 0
                elif yaxis > 252 : yaxis = 252
                if xaxis < 0 : xaxis = 0
                elif xaxis > 240 : xaxis = 240

                value += K * dataset[yaxis, xaxis]

        return value

