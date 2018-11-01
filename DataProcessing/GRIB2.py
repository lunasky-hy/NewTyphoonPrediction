from osgeo import gdal, gdalconst
import numpy as np
import json
import collections as cl
import os


class GRIB2(object):
    def __init__(self, filename):
        self.filename = filename

    # これでＪＳＯＮに保存する
    def saveJSON(self):
        self.initJSON()
        self.convertGRIB2JSON()

        name = self.filename.split(".bin")
        fw = open(name[0] + '.json', 'w')

        # JSON key 用のカウンター
        counter = 0

        ys = cl.OrderedDict()
        for data in self.jsondata:
            ys[str(counter)] = data
            counter += 1

        json.dump(ys, fw, indent = 4)
        del(ys)
        fw.close()

    # JSON形式にコンバート
    def convertGRIB2JSON(self):
        # 取り出す気圧面
        PRESSURES = [100000, 50000, 30000]

        # register drivers
        gdal.AllRegister()
        file_name = self.filename
        
        try:
            # create a data set object
            dataset = gdal.Open(file_name, gdalconst.GA_ReadOnly)

            # 読み込むラスターの情報
            json_dict = gdal.Info(dataset, format='json')


            # 必要なデータの取り出し
            for band in json_dict['bands']:
                band_meta = band['metadata']['']
                if band_meta['GRIB_FORECAST_SECONDS'] != '0 sec':
                    break
                for pressure in PRESSURES:    # 指定された気圧であったら
                    if str(pressure) in band['description']:
                        # 指定された気象要素であったら
                        if 'Geopotential' in band_meta['GRIB_COMMENT']:
                            band_meta = band['metadata']['']
                            array2d = dataset.GetRasterBand(band['band']).ReadAsArray()
                            self.writeJSON(band, array2d)
                            break
                        if 'u-' in band_meta['GRIB_COMMENT']:
                            band_meta = band['metadata']['']
                            array2d = dataset.GetRasterBand(band['band']).ReadAsArray()
                            self.writeJSON(band, array2d)
                            break
                        if 'v-' in band_meta['GRIB_COMMENT']:
                            band_meta = band['metadata']['']
                            array2d = dataset.GetRasterBand(band['band']).ReadAsArray()
                            self.writeJSON(band, array2d)
                            break

        except:
            import traceback
            traceback.print_exc()
            print("Exception!! " + file_name)


    def initJSON(self):
        self.jsondata = []


    def writeJSON(self, info, data):
        info['GPV'] = data.tolist()
        #print(info)
        self.jsondata.append(info)

    def delete(self):
        os.remove(self.filename)

