import numpy as np

class ProbabilityField():
    def __init__(self, ave, var):
        self.lat_ave = ave[0] # 平均
        self.lat_var = var[0] # 分散
        self.long_ave = ave[1]
        self.long_var = var[1]

    def calc(self, lat, long):
        value = 1 / ( 
            2.0 * 3.141592 * np.sqrt(self.lat_var * self.long_var)
            ) * np.exp(
                -0.5 * (((lat - self.lat_ave)**2.0) / self.lat_var + ((long - self.long_ave)**2.0) / self.long_var)
                )
        return value #if value > 0.01 else 0

    def getAverage(self):
        return [self.lat_ave, self.long_ave]

    def getVariance(self):
        return [self.lat_var, self.long_var]