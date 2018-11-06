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

    def __getGPVfromFile__(self, fname, TARGET_BAND_NUM):
        
        fp = open(fname, 'r')
        jsondata = json.load(fp)

        self.dataset = []
        for TARGET in TARGET_BAND_NUM:
            for datas in jsondata.values():
                if datas['band'] == TARGET:
                    info = { 'Pressure' : datas['description'], 'Element' : datas['metadata']['']['GRIB_COMMENT'], 'Dataset' : np.array(datas['GPV'])}
                    self.dataset.append(info)
                    break
        fp.close()