import csv
import numpy as np
import General.PredictMap as pm

def main():
    
    data = np.loadtxt('SampleData\out.csv', dtype = float, delimiter = ",", skiprows = 0)
    positions = []
    colors = []
    for row in data:
        if row[29] > 1000:
            positions.append([row[0], row[1]])
            colors.append('black')

            positions.append([row[4], row[5]])
            colors.append('gray')

            positions.append([row[11], row[12]])
            colors.append('yellow')

            positions.append([row[2], row[3]])
            colors.append('blue')
            #positions.append([[row[2], row[9]], [row[3], row[10]]])

            positions.append([row[23], row[24]])
            colors.append('orange')

            positions.append([row[27], row[28]])
            colors.append('red')
        """
        positions.append([row[0], row[1]])
        if row[29] < 50:
            colors.append('green')
        elif row[29] < 100:
            colors.append('blue')
        elif row[29] < 200:
            colors.append('yellow')
        elif row[29] < 300:
            colors.append('orange')
        elif row[29] < 500:
            colors.append('red')
        elif row[29] < 1000:
            colors.append('Purple')
        else:
            colors.append('black')
        """

    
    
    pm.PredictMap.showOriginals(positions, colors, marker = 'x')

main()