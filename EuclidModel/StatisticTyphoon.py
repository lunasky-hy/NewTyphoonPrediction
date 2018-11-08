import json
import numpy as np

class StatisticTyphoon(object):
    """description of class"""
    def __init__(self, typhoon_dict, TARGET_BAND_NUM):
        self.file = self.__getGPVfromFile__(typhoon_dict['GPVfile'], TARGET_BAND_NUM)
        self.position = [typhoon_dict['latitude'], typhoon_dict['longitude']] 
        self.movement = typhoon_dict['movement']

    def average(self, area):
        return np.average(self.movement[area[0, 0] : area[1, 0], area[0, 1] : area[1, 1]])

    def getMovement(self):
        return self.movement

    # GPVを取得 - OK
    def __getGPVfromFile__(self, fname, TARGET_BAND_NUM):
        
        fp = open(fname, 'r')
        jsondata = json.load(fp)

        self.dataset = []
        for TARGET in TARGET_BAND_NUM:
            for datas in jsondata.values():
                if datas['band'] == TARGET:
                    info = { 'Pressure' : datas['description'], 'Element' : datas['metadata']['']['GRIB_COMMENT'], 'Values' : np.array(datas['GPV'])}
                    self.dataset.append(info)
                    break
        fp.close()

    # 格子間隔のフィルタリング - OK
    def filtering(self, dataset):
        FILTERING_EDGE = [[47, 120], [23, 150]] # 北緯47 東経120からフィルタリング開始
        FILTERING_INTERVAL = 1 # 単位:°
        N = 3 # 中心の周囲Nマスを参照

        ConvertedLatitude = np.arange(FILTERING_EDGE[0][0], FILTERING_EDGE[1][0] - FILTERING_INTERVAL, -1 * FILTERING_INTERVAL)
        ConvertedLongitude = np.arange(FILTERING_EDGE[0][1], FILTERING_EDGE[1][1] + FILTERING_INTERVAL, FILTERING_INTERVAL)

        filtedValues = np.zeros([len(ConvertedLatitude), len(ConvertedLongitude)])

        for latIndex, latValue in enumerate(ConvertedLatitude):
            for longIndex, longValue in enumerate(ConvertedLongitude):

                original = self.__calcGPVIndexes__(latValue, longValue)
                filtedValues[latIndex, longIndex] = self.__Gaussian__(dataset, original, N)

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

                value += K * dataset['Values'][yaxis, xaxis]

        return value

