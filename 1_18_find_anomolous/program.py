import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import accuracy_score, precision_score, f1_score

# Dataset tayyorlash
np.random.seed(42)
anomal_data = np.random.uniform(10, 100, size=(20, 2))
normal_data = np.random.normal(50, 5, size=(580, 2))
data = np.vstack((normal_data, anomal_data))

# plt.scatter(normal_data[:,0], normal_data[:,1], color='blue')
# plt.scatter(anomal_data[:,0], anomal_data[:,1], color='red')
# plt.show()


# Haqiqiy label: normal=1, anomal=-1
true_labels = np.array([1]*580 + [-1]*20)
data = np.hstack((data, true_labels.reshape(600, 1)))
np.savetxt('datasets/testdata4.txt', data, '%.3f %.3f %d')