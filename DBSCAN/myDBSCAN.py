import numpy as np
import matplotlib.pylab as plt
class DBSCAN:
    data = None
    k = None                   
    e = None
    distances_matrix = None    # Obyektlar o'rtasidagi masofalar.
 
    def __init__(self, data, k, e):
        self.data = data
        self.k = k
        self.e = e
        self.distances_matrix = self.setDistancesMatrix()
        
    def setDistancesMatrix(self):
        data = self.data
        rows, _ = np.shape(data)
        distances_matrix = np.zeros((rows, rows))
        for i in range(rows):
            for j in range(i+1, rows):
                d = np.linalg.norm(data[i] - data[j], axis=0)
                distances_matrix[i, j] = d
                distances_matrix[j, i] = d
        return distances_matrix

    def separateGroups(self):   # obyektni o'zi va e radiusdan kichik bo'lgan masofada joylashgan obyektlarni mos guruh qilib birlashtiradi 
        distances_matrix = self.distances_matrix
        rows, _ = np.shape(distances_matrix)
        # [print(distances_matrix[i]) for i in range(rows)]
        e = self.e
        groups = np.zeros(rows, dtype=object)
        for i in range(rows):
            groups[i] = np.where(distances_matrix[i] < e)[0]   # e radiusga teng masofada yotganini olmaydi.
        return groups
    
    def clastering(self):
        distances_matrix = self.distances_matrix
        k = self.k
        rows, _ = np.shape(distances_matrix)
        groups = self.separateGroups()         # Har bir sinf va e radiusdagi obyektlar
        # [print(x,' - ' ,groups[x]) for x in range(rows)]
        result = np.zeros(rows)
        t = 0                                  # Sinf nomi 
        for i in range(rows):
            if result[i] == 0 or result[i] == -1:
                if len(groups[i]) - 1 < k: #  -1. Chunki o'zini chiqarib hisoblashimiz kerak
                    result[i] = -1
                else:
                    t += 1
                    for j in range(rows):
                        if len(np.intersect1d(groups[i], groups[j])) > 0:
                            groups[i] = np.union1d(groups[i], groups[j])
                            if result[j] == 0 or result[j] == -1:
                                result[j] = t
        
        print(np.unique_all(result))
