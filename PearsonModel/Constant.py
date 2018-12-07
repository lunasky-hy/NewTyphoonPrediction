import numpy as np


class Const(object):

    TARGET_BAND = [ [50000, 'Geopotential'], [30000, 'u-'], [30000, 'v-'] ]

    # 過去台風の取り出し
    STATISTIC_DISTANCE = 300 # 現在の台風の中心から300km以内
    COMPARISION_DISTANCE = 1000 # 類似度計算の比較をする範囲を1000kmに設定

    # フィルタリング
    FILTERING_EDGE = [[47, 120], [23, 150]]     # 北緯47 東経120からフィルタリング開始
    FILTERING_INTERVAL = 2  # 単位:°
    N = 3                   # 中心の周囲Nマスを参照
    
    CONVERTED_LATITUDE = np.arange(FILTERING_EDGE[0][0], FILTERING_EDGE[1][0] - FILTERING_INTERVAL, -1 * FILTERING_INTERVAL)
    CONVERTED_LONGITUDE = np.arange(FILTERING_EDGE[0][1], FILTERING_EDGE[1][1] + FILTERING_INTERVAL, FILTERING_INTERVAL)

    # プロット関係
    PLOT_INTARVAL_LAT = 0.1
    PLOT_INTARVAL_LONG = 0.1
    PLOT_START_LAT = 20
    PLOT_END_LAT = 50
    PLOT_START_LONG = 120
    PLOT_END_LONG = 150

    # 誤差修正関係
    DistanceError_6h_12h = 2.1081
    # DistanceError_6h_12h = 2.33590
    K = -29.9565