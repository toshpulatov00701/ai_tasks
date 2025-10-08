import numpy as np
import matplotlib.pyplot as plt


stb_data = np.loadtxt('datasets/stabilitesData.txt', dtype=float)
x = stb_data[:,-1].reshape(-1, 1)
plt.figure(figsize=(10,6))
for i in range(len(stb_data[0]) - 1):
    y = stb_data[:, i].reshape(-1, 1)
    plt.plot(x, y, linewidth=3)
    # plt.legend()
    # plt.title(f'Umumiy grafika')
    plt.xlabel("Показатель масштабирования радиусов")
    plt.ylabel("Устойчивость признака")
    plt.show()