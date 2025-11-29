import numpy as np
from sklearn.cluster import DBSCAN
from myDBSCAN import ClassicDBSCAN
from sklearn.datasets import make_blobs
import time

start_time = time.perf_counter()

X = np.loadtxt('datasets/wine_1.txt', dtype=float)
X = X[:,:-1]
eps = 0.48164513185884156 * 0.7209064582519837
min_samples=15

obj = ClassicDBSCAN(X, eps=eps, min_samples=min_samples, metric_type='euclidean', normal_type='normalization')
u_label = np.unique_all(obj.c_labels)
print(u_label.values, u_label.counts)
# with open('datasets/resultmy.txt', 'w') as ff:
#     pass
# for res in obj.c_labels:
#     with open('datasets/resultmy.txt', 'a') as ff:
#         ff.write(str(res) + '\n')

############################################
## sklearn

def normalize_minus1_plus1(X):
    X_min = X.min(axis=0)
    X_max = X.max(axis=0)
    return 2 * (X - X_min) / (X_max - X_min) - 1

X = normalize_minus1_plus1(X[:-1,:])

db = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean').fit(X)
labels = np.unique_all(db.labels_)
print(labels.values, labels.counts)
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