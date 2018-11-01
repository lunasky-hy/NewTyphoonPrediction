from osgeo import gdal, gdalconst
import numpy as np
import math
import StatisticTyphoon

class SimpleModel(object):
    def __init__(self, GPVfile, position):
        if not (22.4 < float(position[0]) and float(position[0]) < 47.6 and 120 < float(position[1]) and float(position[1]) < 150):
            exit()

        self.__loadGPV__(GPVfile)
        self.position = position
        
        
    def __getStatisticTyphoon__(self):
        fp = open('./typhoon/TyphoonInfo.json', 'r')
        jsondata = json.load(fp)

        self.statisticTyphoons = []
        for index, info in jsondata:
            distance = 6378.137 * math.acos( math.sin(self.position[0]) * math.sin(info['latitude'])
                                           + math.cos(self.position[1]) * math.cos(info['longitude']) * math.cos(info['longitude'] - self.position[1]))
            if distance > 300: # 中心が半径300kmの円の外側だったら飛ばす
                continue
            
            self.statisticTyphoons.append( StatisticTyphoon(info) )

        print('Sample : ' + str(len(self.statisticTyphoons)))

    def __getMoveStat__(self):
        lat = []
        long = []

        for sample in self.statisticTyphoons:
            move = sample.getMovement()
            lat.append(move[0])
            long.append(move[1])

        ave = [ np.average(lat), np.average(long) ]
        var = [ np.var(lat), np.var(long) ]

        return ave, var

    def __loadGPV__(self, file):
        # register drivers
        gdal.AllRegister()
        # create a data set object
        dataset = gdal.Open(file, gdalconst.GA_ReadOnly)
        
        band_num = 1 # 過去データのバンド番号 + 1

        # 読み込むラスターの情報
        bandInfo_dict = gdal.Info(dataset, format='json')
        band = dataset.GetRasterBand(band_num)

        # read the band as matrix
        data_matrix = band.ReadAsArray()
