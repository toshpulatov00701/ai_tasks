import numpy as np
t = np.array([4, 0, 44, 12])
features_length = len(t)
count_combinations = int(features_length * (features_length - 1)/2)
Z_intervals = np.zeros((count_combinations, 4))
print(Z_intervals)