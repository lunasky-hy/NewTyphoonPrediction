from osgeo import gdal, gdalconst
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import functions

class ConvertGRIB2():
    """description of class"""

    def __init__(self):
        """initialize"""
        self.main()

    def main(self):
        # register drivers
        gdal.AllRegister()

        file_name = "Z__C_RJTD_20181010000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin"
        # create a data set object
        dataset = gdal.Open(file_name, gdalconst.GA_ReadOnly)

        col_num = dataset.RasterXSize  # 東西のグリッドの個数-> 0.125 * 241
        row_num = dataset.RasterYSize  # 南北のグリッドの個数-> 0.1 * 253
        band_num = dataset.RasterCount # ラスターの個数
        
        print(col_num)
        print(row_num)
        
        target_band_num = 30 # 読み込むラスターの番号
        band = dataset.GetRasterBand(target_band_num)
        # 読み込むラスターの情報
        json_dict = gdal.Info(dataset, format='json')
        #print(json_dict['bands'][target_band_num - 1])
        #print(gdal.Info(dataset))
        print(band_num)

        # read the band as matrix
        data_matrix = band.ReadAsArray()
        
        #plt.imshow(data_matrix)

        
        fig = plt.figure()
        ax = fig.add_subplot(2, 1, 1, projection='3d')
        bx = fig.add_subplot(2, 1, 2, projection='3d')
        
        X1, Y1 = np.meshgrid(np.arange(120, 150.125, 0.125), np.arange(47.6, 22.3, -0.1))
        X2, Y2 = np.meshgrid(np.arange(120, 120 + (0.125 * 7) * 34, 0.125 * 7), np.arange(47.6, 47.6 + (-0.1 * 7) * 36, -0.1 * 7))
        
        u_wind = []
        v_wind = []
        # 必要なデータの取り出し
        for band in json_dict['bands']:
            if('50000[Pa]' in band['description']):
                band_meta = band['metadata']['']
                if(band_meta['GRIB_FORECAST_SECONDS'] != '0 sec'):
                    break
                #if('Geopotential height' in band_meta['GRIB_COMMENT']):
                if('u-' in band_meta['GRIB_COMMENT']):
                    print(band)
                    array2d = dataset.GetRasterBand(band['band']).ReadAsArray()
                    ax.plot_surface(X1, Y1, array2d, cmap='bwr')
                    ax.set_title(band_meta['GRIB_COMMENT'])
                    arr = functions.GaussianFilter(array2d)
                    bx.plot_surface(X2, Y2, arr, cmap='bwr')



        # データの取り出しと比較表示
        """
        fig = plt.figure()
        ax = fig.add_subplot(2, 2, 1, projection='3d')
        bx = fig.add_subplot(2, 2, 2, projection='3d')
        cx = fig.add_subplot(2, 2, 3, projection='3d')
        
        X, Y = np.meshgrid(np.arange(120, 150.125, 0.125), np.arange(47.6, 22.3, -0.1))

        u_wind = []
        v_wind = []
        # 必要なデータの取り出し
        for band in json_dict['bands']:
            if('30000[Pa]' in band['description']):
                band_meta = band['metadata']['']
                if(band_meta['GRIB_FORECAST_SECONDS'] != '0 sec'):
                    break
                if('Geopotential height' in band_meta['GRIB_COMMENT']):
                    print(band)
                    ax.plot_surface(X, Y, dataset.GetRasterBand(band['band']).ReadAsArray(), cmap='bwr')
                    ax.set_title('Geopotential Height [gpm]')
                if('u-' in band_meta['GRIB_COMMENT']):
                    print(band)
                    u_wind = dataset.GetRasterBand(band['band']).ReadAsArray()
                    bx.plot_surface(X, Y, u_wind, cmap='bwr')
                    bx.set_title('u-wind(east-west) [m/s]')
                if('v-' in band_meta['GRIB_COMMENT']):
                    print(band)
                    v_wind = dataset.GetRasterBand(band['band']).ReadAsArray()
                    cx.plot_surface(X, Y, v_wind, cmap='bwr')
                    cx.set_title('v-wind(north-south) [m/s]')
        
        wind = np.zeros([row_num, col_num])
        for x in range(row_num):
            for y in range(col_num):
                wind[x, y] = np.sqrt(pow(u_wind[x, y], 2) + pow(v_wind[x, y], 2))
        dx = fig.add_subplot(2, 2, 4, projection='3d')
        dx.plot_surface(X, Y, wind, cmap='bwr')
        dx.set_title('wind [m/s]')
        """


        
        plt.show()