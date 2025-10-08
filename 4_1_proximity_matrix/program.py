import numpy as np
arr = np.random.randint(1, 6, size=(100, 30))
classes = np.random.randint(1, 4, size=(100,1))
res_data = np.hstack((arr, classes))
# np.savetxt('datasets/testdata.txt', res_data, fmt='%d')
# print(res_data)

# arr = np.random.randint(10, 100, size=(15, 15))
