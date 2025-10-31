# Ushbu versiyada bir nechta k(2, 3, 4, 5, 6) lar uchun tekshirish mumkin.
import numpy as np
from dbscan3Type import DBSCAN3Type

data = np.loadtxt('datasets/dogwolfdata.txt', dtype=float)
n = 6  # 2, 3, 4...n
objDb = DBSCAN3Type(data, n, metric_type='euclidean', normal_type='normalization')

###################################
# Ekstrimumlarni topish

# stb_data = np.loadtxt('datasets/stabilitesData.txt', dtype=float)
# eks_lambda = np.zeros(len(stb_data[0]) - 1)
# for i in range(len(stb_data[0]) - 1):
#     ekstrimum_min = np.min(stb_data[:,i])
#     ekstrimum_min_index = np.argmin(stb_data[:,i])
#     eks_lambda[i] = stb_data[ekstrimum_min_index, -1]

# t = objDb.e_avarages_K
# print(t)
# print(eks_lambda)
# eks = t * eks_lambda
# print(eks)