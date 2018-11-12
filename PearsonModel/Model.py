from osgeo import gdal, gdalconst
import numpy as np
import json
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.basemap import Basemap
import PearsonModel.StatisticTyphoon as typ
import PearsonModel.ProbabilityField as pf
from PearsonModel.Constant import Const

class ModelMain(object):
    # OK
    def __init__(self, GPVfile, position):
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            exit()

        print("Loading")
        self.__loadGPV__(GPVfile, Const.TARGET_BAND)
        print("Loading... Complete")
        self.position = position

    def processing(self):
        print("Statistic Typhoon Loading...")
        self.__getStatisticTyphoon__()
        print("Statistic Typhoon Loading... Complete")
        print("Create Probability Field...")
        self.__getProbabilityField__()
        print('Finish Processing')

    # グラフの描画
    def plotGraph(self):        
        fig = plt.figure()
        
        X = np.arange(Const.PLOT_START_LONG, Const.PLOT_END_LONG + Const.PLOT_INTARVAL_LONG, Const.PLOT_INTARVAL_LONG)
        Y = np.arange(Const.PLOT_START_LAT, Const.PLOT_END_LAT + Const.PLOT_INTARVAL_LAT, Const.PLOT_INTARVAL_LAT)
        values = np.zeros([len(Y), len(X)])
        full = 0

        for row in range(len(Y)):
            for colum in range(len(X)):
                values[row, colum] = self.field.calc(Y[row], X[colum])
                full += values[row, colum]
        print(full)

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

        plt.show()

    # 確率場の算出用
    def __getProbabilityField__(self):
        ave, var = self.__getMoveStat__()
        ave = [ave[0] + self.position[0], ave[1] + self.position[1]]
        self.field = pf.ProbabilityField(ave, var)

    # 過去台風のロード部分 - OK
    def __getStatisticTyphoon__(self):
        fp = open('./typhoon/TyphoonInfo.json', 'r')
        jsondata = json.load(fp)

        self.statisticTyphoons = []
        del(jsondata['comment'])
        for index, info in jsondata.items():
            distance = self.__GlobalDistance__(self.position, [info['latitude'], info['longitude']])
            if distance > Const.STATISTIC_DISTANCE: # 中心が半径300kmの円の外側だったら飛ばす
                continue
            
            self.statisticTyphoons.append( typ.StatisticTyphoon(info, self.target_bandnum) )
            print(str(len(self.statisticTyphoons)) + ':' + str(info['GPVfile']))

        print('Sample : ' + str(len(self.statisticTyphoons)))

    # 平均,分散の算出 - OK
    def __getMoveStat__(self):
        # 比較する範囲を設定
        INDEXES = []
        for latIndex, latValue in enumerate(Const.CONVERTED_LATITUDE):
            for longIndex, longValue in enumerate(Const.CONVERTED_LONGITUDE):
                if self.__GlobalDistance__(self.position, [latValue, longValue]) < Const.COMPARISION_DISTANCE:
                    INDEXES.append([latIndex, longIndex])
        
        total = 0.0
        # 比較し係数を過去モデルに保存
        for index, smodel in enumerate(self.statisticTyphoons):
            for bandIndex in range(len(smodel.dataset)):
                smodel.calcAnalogy(self.bandset, bandIndex, INDEXES)
            total += smodel.aveAnalogy()
            print(str(index) + " : " + str(smodel.getAveAnalogy() * 100) + '%')

        ave = [0.0, 0.0]
        lat = []
        long = []
        for smodel in self.statisticTyphoons:
            move = smodel.getMovement()
            lat.append(move[0])
            long.append(move[1])
            ave[0] += (smodel.getAveAnalogy() / total) * move[0]
            ave[1] += (smodel.getAveAnalogy() / total) * move[1]

        var = [np.var(lat), np.var(long)]
        return ave, var

    # GPV値のロード - OK
    def __loadGPV__(self, file, TARGET_BAND):
        # register drivers
        gdal.AllRegister()
        # create a data set object
        dataset = gdal.Open(file, gdalconst.GA_ReadOnly)
        
        band_num = 1 # 過去データのバンド番号 + 1

        # 読み込むラスターの情報
        bandInfo_dict = gdal.Info(dataset, format='json')
        # バンド情報格納配列を初期化
        self.bandset = []
        # バンド番号の保持 -> 過去台風データ取り出しに使用
        self.target_bandnum = []

        # 各バンド情報からTARGET_BANDにあう情報を見つける
        for info in bandInfo_dict['bands']:
            meta = info['metadata']['']
            if meta['GRIB_FORECAST_SECONDS'] != '0 sec':
                break
            # ターゲットバンドの探索
            for TARGET in TARGET_BAND:
                if str(TARGET[0]) in info['description'] and TARGET[1] in meta['GRIB_COMMENT']:
                    data_dict = {}
                    data_dict['Pressure'] = info['description']
                    data_dict['Element'] = meta['GRIB_COMMENT']
                    # 格子点データをndarrayにして入れる
                    self.target_bandnum.append(int(info['band']))
                    data_dict['Value'] = self.__filtering__(dataset.GetRasterBand(info['band']).ReadAsArray())
                    self.bandset.append(data_dict)

    # 2点間の距離の算出 - OK
    def __GlobalDistance__(self, pos1, pos2):
        R = 6378.1370
        
        lat1 = math.radians(pos1[0])
        long1 = math.radians(pos1[1])
        lat2 = math.radians(pos2[0])
        long2 = math.radians(pos2[1])

        averageLat = (lat1 - lat2) / 2
        averageLong = (long1 - long2) / 2

        return R * 2 * math.asin( math.sqrt(math.pow( math.sin(averageLat), 2) + math.cos(lat1) * math.cos(lat2) * math.pow( math.sin(averageLong), 2)))

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