import numpy as np

class DistMetrics:
    def __init__(self, data, metric_type, normal_type=None):
        self.metric_type = metric_type
        self.normal_type = normal_type
        rows, _ = np.shape(data)
        self.m = rows - 1                                             # Obyektlar soni
        self.characteristic_vector = data[-1,:].astype(int)           # Alomat turini ko'rsatuvchi vektor. 0 - nominal, 1 - miqdoriy
        
        if normal_type == None:
            self.normal_data = data[:-1,:]                            # Normalizatsiya berilgan bo'lsa, normalizatsiyadan keyingi data. Berilmagan bo'lsa dastlabki data.
        elif normal_type == 'normalization':
            self.normal_data = self.normalize(data[:-1,:])
        
        if metric_type == 'euclidean':
            self.distance_matrix = self.euclidean_square()
        elif metric_type == 'chebyshev':
            self.distance_matrix = self.chebyshev()
        elif metric_type == 'juravlov':
            self.distance_matrix = self.juravlov()
        else:
            raise ValueError(f"Metrika turi noto'g'ri: {metric_type}")
    
    def normalize(self, data):                                # [-1, 1] oraliqqa tushirish
        mask = self.characteristic_vector == 1
        
        if np.any(mask):
            dmin = np.min(data[:, mask], axis=0)
            dmax = np.max(data[:, mask], axis=0)
            denom = dmax - dmin
            denom[denom == 0] = 1
            data[:, mask] = 2 * (data[:, mask] - dmin) / denom - 1

        return data
    
    def euclidean(self):
        if np.any(self.characteristic_vector == 0):
            raise ValueError("Evklid metrikasi nominal ustunlarga ruxsat bermaydi.")

        data = self.normal_data
        m = self.m
        distance_matrix = np.zeros((m, m))
        
        for i in range(m):
            distance_matrix[i] = np.linalg.norm(data[i] - data, axis=1)
        return distance_matrix
        
    def euclidean_square(self):                               # Aniqlik va tezlikni oshirish uchun
        if np.any(self.characteristic_vector == 0):
            raise ValueError("Evklid metrikasi nominal ustunlarga ruxsat bermaydi.")

        data = self.normal_data
        m = self.m
        distance_matrix = np.zeros((m, m))
        for i in range(m):
            distance_matrix[i] = np.sum((data[i] - data)**2, axis=1)
        return distance_matrix

    def chebyshev(self):
        if np.any(self.characteristic_vector == 0):
            raise ValueError("Chebyshev metrikasi nominal ustunlarga ruxsat bermaydi.")
        
        data = self.normal_data
        m = self.m
        distance_matrix = np.zeros((m, m))
        for i in range(m):
            distance_matrix[i] = np.max(np.abs(data[i] - data), axis=1)
        return distance_matrix
    
    def juravlov(self):
        characteristic_vector = self.characteristic_vector
        data = self.normal_data
        m = self.m
        q_arr_1 = characteristic_vector == 1
        q_arr_0 = characteristic_vector == 0
        distance_matrix = np.zeros((m, m))
        q_sum = 0
        for i in range(m):
            if np.any(q_arr_1 == True):
                q_sum = np.max(np.abs(data[i, q_arr_1] - data[:, q_arr_1]), axis=1)
            n_sum = np.sum(data[i, q_arr_0]!=data[:, q_arr_0], axis=1)
            distance_matrix[i] = q_sum + n_sum
        return distance_matrix

# data = np.loadtxt('datasets/testdata2.txt', dtype=float)
# metric_type='euclidean'
# normal_type='normalization'

# obj = DistMetrics(data=data, metric_type=metric_type, normal_type=normal_type)
# print(obj.distance_matrix)
    
# SINF TARIFI
# Sinfga 3 ta parametr keladi. 1 - berilganlar, 2 - matrika turi, 3 - normalizatsiya

# Berilganlarga quyidagi standart ko'rinishida kelishi kerak:
# 1. Obyektlar kesishmaydigan va takrorlanmaydigan
# 2. Tushirib qoldirilgan alomat bironta ham obyektda uchramaydi
# 3. Berilganlar o'qituvchisiz(unlabled) bo'lishi
# 4. Harakteristik vektor mavjud va unda 0 - nominal, 1 - miqdoriy bo'lishi
# 5. Agar turli tipdagi berilganlar bo'lsa, metrika 'juravlov' bo'lishi