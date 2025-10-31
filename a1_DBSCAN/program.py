import numpy as np
from sklearn.cluster import DBSCAN
from myDBSCAN import ClassicDBSCAN
from sklearn.datasets import make_blobs
import time

start_time = time.perf_counter()

X = np.loadtxt('datasets/uzbkares.txt', dtype=float)
eps = 0.128
min_samples=5

obj = ClassicDBSCAN(X, eps=eps, min_samples=min_samples, metric_type='juravlov')
with open('datasets/resultmy.txt', 'w') as ff:
    pass
for res in obj.c_labels:
    with open('datasets/resultmy.txt', 'a') as ff:
        ff.write(str(res) + '\n')

############################################
## sklearn

# db = DBSCAN(eps=eps, min_samples=min_samples).fit(X[:-1,:])
# labels = db.labels_
# core_indices = db.core_sample_indices_
# status = np.array([2] * len(X[:-1,:]))
# status[core_indices] = 1
# status[labels == -1] = 3
# # print(status)
# with open('datasets/resultskt.txt', 'w') as ff:
#     pass
# for res in labels:
#     with open('datasets/resultskt.txt', 'a') as ff:
#         ff.write(str(res) + '\n')

# print('statuslar bir-biriga tenglari:', np.sum(obj.getStatuses() == status))
# print('klasterlar farqlilari:', np.sum(obj.c_labels != labels))

############################################
## Dataset yaratish
# data, _ = make_blobs(
#     n_samples=5000,
#     centers=10,
#     n_features=50,
#     cluster_std=9,
#     center_box=(0, 1000),
#     random_state=42
#     )
# np.savetxt('datasets/data5000x50.txt', data, fmt='%g')

############################################

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f'Sarflangan vaqt: {elapsed_time: .4f}')