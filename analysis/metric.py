import pandas as pd
from datetime import datetime
import json

from scipy import stats
from uti import utility
from data import dataOperation


def averageError(matrix1, matrix2):
    l = len(matrix1[0])
    totalerror= 0
    n = 0
    for i in range(l):
        for j in range(l):
            if i!=j:
                dif = abs(matrix1[i][j] - matrix2[i][j])
                error = dif/max(matrix1[i][j],matrix2[i][j])
                totalerror+=error
                n+=1
    return totalerror/n


def pearsoner(matrix1, matrix2):
    l = len(matrix1[0])
    l1 = []
    l2 = []
    for i in range(l):
        for j in range(l):
            if i!=j:
                l1.append(matrix1[i][j])
                l2.append(matrix2[i][j])

    return stats.pearsonr(l1, l2)







if __name__ == '__main__':
    A = pd.np.random.rand(4, 4)
    B = pd.np.random.rand(4, 4)
    print(pearsoner(A,A))
    print(pearsoner(A, B))
