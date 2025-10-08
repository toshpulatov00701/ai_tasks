import numpy as np
import dbscan3Type
import myRelFun

data = np.loadtxt('datasets/ionosphere.txt', dtype=float)
n = 6  # 2, 3, 4...n
objDb = dbscan3Type.myDBSCAN(data, n, 'euclidean', 'normalization')
# print(objDb.lambda_min_max)
# objDb.possibleLambdaes()
# objDb.buildStabilityData()



###################################

# t = objDb.e_avarages_K
# eks = t * objDb.findOptimalLambda()
# print(eks)

###################################
# Ekstrimumlarni topish
stb_data = np.loadtxt('datasets/stabilitesData.txt', dtype=float)
eks_lambda = np.zeros(len(stb_data[0]) - 1)
for i in range(len(stb_data[0]) - 1):
    ekstrimum_min = np.min(stb_data[:,i])
    ekstrimum_min_index = np.argmin(stb_data[:,i])
    eks_lambda[i] = stb_data[ekstrimum_min_index, -1]

t = objDb.e_avarages_K
print(t)
print(eks_lambda)
eks = t * eks_lambda
print(eks)