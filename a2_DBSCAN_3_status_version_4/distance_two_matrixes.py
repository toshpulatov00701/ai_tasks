import numpy as np

class DTMatrixes:
    # normal_data_1         - Normalizatsiya berilgan bo'lsa, normalizatsiyadan keyingi data. Berilmagan bo'lsa dastlabki data.
    # normal_data_2         - Normalizatsiya berilgan bo'lsa, normalizatsiyadan keyingi data. Berilmagan bo'lsa dastlabki data.
    # data_1_m              - Birinchi data obyektlar soni
    # data_2_m              - Ikkinchi data obyektlar soni
    # characteristic_vector - Alomat turini ko'rsatuvchi vektor. 0 - nominal, 1 - miqdoriy

    def __init__(self, data_1, data_2, metric_type, normal_type=None):
        self.metric_type = metric_type
        rows, _ = np.shape(data_1)
        self.data_1_m = rows - 1
        rows, _ = np.shape(data_2)
        self.data_2_m = rows - 1
        self.characteristic_vector = data_1[-1,:]

        if normal_type == None:
            self.normal_data_1 = data_1[:-1,:]
            self.normal_data_2 = data_2[:-1,:]
        elif normal_type == 'normalization':
            self.normal_data_1 = self.normalize(data_1[:-1,:])
            self.normal_data_2 = self.normalize(data_2[:-1,:])

        if metric_type == 'euclidean':
            self.distance_matrix = self.euclidean_square()
        elif metric_type == 'chebyshev':
            self.distance_matrix = self.chebyshev()
        elif metric_type == 'juravlov':
            self.distance_matrix = self.juravlov()
    
    def normalize(self, data):    # [-1, 1] oraliqqa tushirish
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
                
        data_1 = self.normal_data_1
        data_2 = self.normal_data_2
        m_1 = self.data_1_m
        m_2 = self.data_2_m
        distance_matrix = np.zeros((m_1, m_2))
        for i in range(m_1):
            distance_matrix[i] = np.linalg.norm(data_1[i] - data_2, axis=1)
        return distance_matrix

    def euclidean_square(self):                # Aniqlik va tezlikni oshirish uchun
        if np.any(self.characteristic_vector == 0):
            raise ValueError("Evklid metrikasi nominal ustunlarga ruxsat bermaydi.")
        
        data_1 = self.normal_data_1
        data_2 = self.normal_data_2
        m_1 = self.data_1_m
        m_2 = self.data_2_m
        distance_matrix = np.zeros((m_1, m_2))
        for i in range(m_1):
            distance_matrix[i] = np.sum((data_1[i] - data_2)**2, axis=1)
        return distance_matrix
 
    def chebyshev(self):
        if np.any(self.characteristic_vector == 0):
            raise ValueError("Evklid metrikasi nominal ustunlarga ruxsat bermaydi.")
        
        data_1 = self.normal_data_1
        data_2 = self.normal_data_2
        m_1 = self.data_1_m
        m_2 = self.data_2_m
        distance_matrix = np.zeros((m_1, m_2))
        for i in range(m_1):
            distance_matrix[i] = np.max(np.abs(data_1[i] - data_2), axis=1)
        return distance_matrix

    def juravlov(self):
        characteristic_vector = self.characteristic_vector
        data_1 = self.normal_data_1
        data_2 = self.normal_data_2
        m_1 = self.data_1_m
        m_2 = self.data_2_m
        distance_matrix = np.zeros((m_1, m_2))
        q_arr_1 = characteristic_vector == 1
        q_arr_0 = characteristic_vector == 0
        q_sum = 0
        for i in range(m_1):
            if np.any(q_arr_1 == True):
                q_sum = np.max(np.abs(data_1[i, q_arr_1] - data_2[:, q_arr_1]), axis=1)
            n_sum = np.sum(data_1[i, q_arr_0]!=data_2[:, q_arr_0], axis=1)
            distance_matrix[i] = q_sum + n_sum
        return distance_matrix

# arr_1 = np.array([
#     [2, 2, 4],
#     [5, 1, 1],
#     [9, 1, 3],
#     [6, 1, 8],
#     [1, 1, 1]
# ])

# arr_2 = np.array([
#     [1, 2, 3],
#     [5, 2, 7],
#     [2, 1, 5],
#     [1, 1, 1]
# ])

# obj = DTMatrixes(arr_1, arr_2, 'euclidean')
# print(obj.distance_matrix)

# SINF TARIFI
# Sinfga 3 ta parametr keladi. 1 - berilganlar, 2 - matrika turi, 3 - normalizatsiya.

# Vazifasi:
# data_1'ning har bir elementidan data_2'gacha bo'lgan masofalardan tuzilgan matritsa 

# Berilganlarga quyidagi standart ko'rinishida kelishi kerak:
# 1. Obyektlar kesishmaydigan va takrorlanmaydigan
# 2. Tushirib qoldirilgan alomat bironta ham obyektda uchramaydi
# 3. Berilganlar o'qituvchisiz(unlabled) bo'lishi
# 4. Harakteristik vektor mavjud va unda 0 - nominal, 1 - miqdoriy bo'lishi
# 5. Agar turli tipdagi berilganlar bo'lsa, metrika 'juravlov' bo'lishi