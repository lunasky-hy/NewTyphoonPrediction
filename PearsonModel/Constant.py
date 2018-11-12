import numpy as np


class Const(object):

    TARGET_BAND = [ [100000, 'Geopotential'], [50000, 'u-'], [50000, 'v-'] ]

    # 過去台風の取り出し
    STATISTIC_DISTANCE = 300 # 現在の台風の中心から300km以内
    COMPARISION_DISTANCE = 1000 # 類似度計算の比較をする範囲を1000kmに設定

    # フィルタリング
    FILTERING_EDGE = [[47, 120], [23, 150]]     # 北緯47 東経120からフィルタリング開始
    FILTERING_INTERVAL = 1  # 単位:°
    N = 3                   # 中心の周囲Nマスを参照
    
    CONVERTED_LATITUDE = np.arange(FILTERING_EDGE[0][0], FILTERING_EDGE[1][0] - FILTERING_INTERVAL, -1 * FILTERING_INTERVAL)
    CONVERTED_LONGITUDE = np.arange(FILTERING_EDGE[0][1], FILTERING_EDGE[1][1] + FILTERING_INTERVAL, FILTERING_INTERVAL)

