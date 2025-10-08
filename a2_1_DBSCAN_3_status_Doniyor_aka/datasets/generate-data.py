import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# data = np.loadtxt('datasets/uzbkares.txt', dtype=int)
data = np.loadtxt('datasets/ionosphere.txt', dtype=float)
# data = np.loadtxt('datasets/dogwolfdata.txt', dtype=float)
# data = np.loadtxt('datasets/testdata.txt', dtype=float)
scaler = MinMaxScaler(feature_range=(-1, 1))
X = data[:-1,:]
X = scaler.fit_transform(X)
# eks = np.array([0.08030034, 0.10264829, 0.11642883, 0.13048989, 0.1431861,  0.15690148, 0.16739541, 0.17714575, 0.18734651])
eks = np.array([0.79439412, 0.79449314, 0.79408833, 0.79481821, 0.79588553])
for i in range(len(eks)):
    
    db = DBSCAN(eps=eks[i], min_samples=3 + i, metric='euclidean').fit(X)
    db_lables = db.labels_
    
    
    print(f'k = {i + 2}')
    print('Klasterlar: ',np.unique_all(db_lables).values)
    print('Har bir klaster miqdori: ', np.unique_all(db_lables).counts)
    all_claster_count = len(np.unique_all(db_lables).counts)
    
    # Har bir klasterlardagi yadroviy va chegaraviylar miqdori
    core_mask = np.zeros_like(db_lables, dtype=bool)    # yadro nuqtalar maskasi
    core_mask[db.core_sample_indices_] = True
    clusters = [c for c in np.unique(db_lables) if c != -1]
    if np.unique_all(db_lables).values[0] == -1: all_claster_count -= 1
    print('Umumiy klaster soni:', all_claster_count)
    t = ''
    for c in clusters:
        in_c = (db_lables == c)
        core_c = np.sum(core_mask & in_c)
        border_c = np.sum(in_c) - core_c
        t+=f'{core_c}/{border_c}, '
    print('Klasterlar taqsimoti[yadroviy/chegaraviy]: ', t)
    


# data, _ = make_blobs(
#     n_samples=150,
#     centers=3,
#     n_features=2,
#     cluster_std=9,
#     center_box=(0, 100),
#     random_state=42
#     )
# np.savetxt('datasets/testdata.txt', data, fmt='%g')
# data = np.loadtxt('datasets/testdata.txt', dtype=float)
# plt.figure(figsize=(6, 6))
# plt.scatter(data[:, 0], data[:, 1], c='blue', s=50)
# plt.title("make_blobs bilan yaratilgan ma'lumotlar (3 klaster)")
# plt.xlabel("X1")
# plt.ylabel("X2")
# plt.show()

###############################################

