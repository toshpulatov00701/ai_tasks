import numpy as np
from distanceMetrics import dMetrics

X = np.loadtxt('datasets/testdata3.txt', dtype=float)
obj = dMetrics(X, metric_type='juravlov')
print(obj.distance_matrix)
