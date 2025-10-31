import numpy as np
import matplotlib.pyplot as plt
from myDBSCAN import ClassicDBSCAN
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN

####################################################
## Skitlearn guruhlarga ajralganligini tekshirish

# data = np.loadtxt('datasets/ionosphere.txt', dtype=float)
# scaler = MinMaxScaler(feature_range=(-1, 1))
# X_normalized = scaler.fit_transform(data[:-1,:])
# # X = data
# eks = 1.4503261038632527
# db = DBSCAN(eps=eks, min_samples=6)
# db.fit(X_normalized)
# db_lables = db.labels_
# # print(db_lables)
# print()
# print(f'k = {6}')
# print('clasterlar: ',np.unique_all(db_lables).values)
# print('har bir claster miqdori: ', np.unique_all(db_lables).counts)
# all_claster_count = len(np.unique_all(db_lables).counts)
# if np.unique_all(db_lables).values[0] == -1: all_claster_count -= 1
# print('Umumiy klaster soni:', all_claster_count)


############################################################

# import numpy as np
# from sklearn.datasets import make_blobs
# import matplotlib.pyplot as plt

# Ma'lumotlar to'plamini generatsiya qilish
# X, y = make_blobs(
#     n_samples=150,    # Obyektlar soni (150 ta)
#     n_features=2,     # Alomatlar soni (2 ta)
#     centers=3,        # Klasterlar soni (3 ta)
#     cluster_std=1,  # Klasterlarning standart og'ishmasi (tarqalishi)
#     random_state=42   # Natijalarning takrorlanuvchanligi uchun
# )

# np.savetxt('datasets/testdata2.txt', X, fmt="%g", delimiter=' ')

# Ma'lumotlarni vizualizatsiya qilish (ixtiyoriy)
# plt.figure(figsize=(8, 6))
# # Har bir klaster uchun rang berish
# for i in range(3):
#     plt.scatter(
#         X[y == i, 0],
#         X[y == i, 1],
#         s=50,
#         label=f'Klaster {i}'
#     )
# plt.title('Generatsiya Qilingan 3 Klasterli Dataset')
# plt.xlabel('Alomat 1')
# plt.ylabel('Alomat 2')
# plt.legend()
# plt.grid(True)
# plt.show()