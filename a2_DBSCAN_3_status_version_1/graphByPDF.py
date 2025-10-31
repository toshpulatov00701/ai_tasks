import numpy as np
import matplotlib.pyplot as plt
from myDBSCAN import ClassicDBSCAN

#####################################################
# Grafikani tekshirish

stb_data = np.loadtxt('datasets/stabilitesData.txt', dtype=float)
x = stb_data[:,-1].reshape(-1, 1)
plt.figure(figsize=(10,6))
for i in range(len(stb_data[0]) - 1):
    y = stb_data[:, i].reshape(-1, 1)
    plt.plot(x, y, linewidth=3, label=f'k = {i + 2}')    
    plt.legend()
    # plt.plot(x, y, linewidth=3)    
    # plt.title(f'k = {i + 2}')
    plt.xlabel("Показатель масштабирования радиусов")
    plt.ylabel("Устойчивость признака")
    plt.show()


#####################################################
# Guruhlarga ajralganligini tekshirish

# data = np.loadtxt('datasets/dogwolfdata.txt', dtype=float)

# eks = np.array([0.31685447, 0.46014863, 0.56700935, 0.58695027, 0.62877592])
# for i in range(len(eks)):
#     db = ClassicDBSCAN(X, eps=eks[i], min_samples=i + 2, metric_type='euclidean', normal_type='normalization')
#     db_lables = db.c_labels
#     print()
#     print(f'k = {i + 2}')
#     print('clasterlar: ',np.unique_all(db_lables).values)
#     print('har bir claster miqdori: ', np.unique_all(db_lables).counts)
#     all_claster_count = len(np.unique_all(db_lables).counts)
#     if np.unique_all(db_lables).values[0] == -1: all_claster_count -= 1
#     print('Umumiy klaster soni:', all_claster_count)