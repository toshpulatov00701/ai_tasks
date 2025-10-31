# Ushbu versiyada fiksirlangan k uchun. Anomallar % ko'rsatkichi ko'rsatilmaydi. Derixlega nisbatan topadi.

import numpy as np
from dbscan3Type import DBSCAN3Type

data = np.loadtxt('datasets/ionosphere.txt', dtype=float)
n = 6
objDb = DBSCAN3Type(data, n, metric_type='euclidean', normal_type='normalization')
print(objDb.lambda_min_max)

print('4.1=>',np.sum(objDb.setStatus(objDb.e_avarages_K * 4.1) == 3))

###################################
# Ekstrimumlarni topish
# eks = np.array([0.39704933, 0.41200455, 0.39781382, 0.38256659, 0.40152474])
# print(objDb.e_avarages_K)
# print(objDb.e_avarages_K * eks)
