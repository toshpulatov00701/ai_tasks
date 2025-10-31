import numpy as np
import matplotlib.pyplot as plt
from myDBSCAN import ClassicDBSCAN

#####################################################
# Grafikani tekshirish

# stb_data = np.loadtxt('datasets/stabilitesData.txt', dtype=float)
# x = stb_data[:,-1].reshape(-1, 1)
# plt.figure(figsize=(10,6))
# for i in range(len(stb_data[0]) - 1):
#     y = stb_data[:, i].reshape(-1, 1)
#     # plt.plot(x, y, linewidth=3, label=f'k = {i + 2}')    
#     # plt.legend()
#     plt.plot(x, y, linewidth=3)    
#     plt.title(f'k = {i + 2}')
#     plt.xlabel("Показатель масштабирования радиусов")
#     plt.ylabel("Устойчивость признака")
#     plt.show()


#####################################################
# Guruhlarga ajralganligini tekshirish

# data = np.loadtxt('datasets/ionosphere.txt', dtype=float)

# eks = 0.8904275662258616
# # data = data[:,:-1]
# min_samples = 6

# db = ClassicDBSCAN(data, eps=eks, min_samples=min_samples, metric_type='euclidean', normal_type='normalization')
# db_lables = db.c_labels
# # print()
# print('clasterlar: ',np.unique_all(db_lables).values)
# print('har bir claster miqdori: ', np.unique_all(db_lables).counts)
# all_claster_count = len(np.unique_all(db_lables).counts)
# if np.unique_all(db_lables).values[0] == -1: all_claster_count -= 1
# print('Umumiy klaster soni:', all_claster_count)

