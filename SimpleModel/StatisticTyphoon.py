import json
import numpy as np

class StatisticTyphoon(object):
    """description of class"""
    def __init__(self, typhoon_dict):
        self.file = self.__getGPVfromFile__(typhoon_dict['GPVfile'])
        self.position = [typhoon_dict['latitude'], typhoon_dict['longitude']] 
        self.movement = typhoon_dict['movement']

    def average(self, area):
        return np.average(self.movement[area[0, 0] : area[1, 0], area[0, 1] : area[1, 1]])

    def getMovement(self):
        return self.movement

    def __getGPVfromFile__(self, fname):
        band_num = 0
        
        fp = open(file, 'r')
        jsondata = json.load(fp)

        self.band_meta = jsondata[str(band_num)]['metadata']['']       # 1000hPa高度
        self.data = np.array(jsondata[str(band_num)]['GPV'])