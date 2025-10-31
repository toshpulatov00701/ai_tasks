import numpy as np

class dMetrics:
    normal_data = None               # Normalizatsiya berilgan bo'lsa, normalizatsiyadan keyingi data. Berilmagan bo'lsa dastlabki data.
    distance_matrix = None
    m = None                         # Obyektlar soni
    characteristic_vector = None     # Alomat turini ko'rsatuvchi vektor. 0 - nominal, 1 - miqdoriy

    def __init__(self, data, metric_type, normal_type=None):
        rows, _ = np.shape(data)
        self.m = rows - 1
        self.characteristic_vector = data[-1,:]
        if normal_type == None:
            self.normal_data = data[:-1,:]   
        elif normal_type == 'normalization':
            self.normal_data = self.normalizationData(data[:-1,:])

        if metric_type == 'euclidean':
            self.distance_matrix = self.distanceMatrixEuclideanSquare()
        elif metric_type == 'chebyshev':
            self.distance_matrix = self.distanceMatrixChebyshev()
        elif metric_type == 'juravlov':
            self.distance_matrix = self.distanceMatrixJuravlov()
    
    def normalizationData(self, data):    # [-1, 1] oraliqqa tushirish
        characteristic_vector = self.characteristic_vector
        rows, cols = np.shape(data)
        re_data = np.zeros((rows, cols), dtype=float)
        for j in range(cols):
            by_col_min = np.min(data[:,j])
            by_col_max = np.max(data[:,j])
            denomirator = by_col_max - by_col_min
            for i in range(rows):
                if characteristic_vector[j] == 1:
                    re_data[i, j] = 2 * (data[i, j] - by_col_min) / denomirator - 1
                else:
                    re_data[i, j] = data[i, j]
        return re_data
    
    def distanceMatrixEuclidean(self):
        characteristic_vector = self.characteristic_vector
        try:
            if np.sum(characteristic_vector == 0) >= 1:
                raise ValueError('Evklid metrikasida nominal alomatlar bo\'lishi mumkin emas.')
            data = self.normal_data
            m = self.m
            distance_matrix = np.zeros((m, m))
            for i in range(m):
                distance_matrix[i] = np.linalg.norm(data[i] - data, axis=1)
            return distance_matrix
        except ValueError as e:
            print('Xatolik:', e)

    def distanceMatrixEuclideanSquare(self):                # Aniqlik va tezlikni oshirish uchun
        characteristic_vector = self.characteristic_vector
        try:
            if np.sum(characteristic_vector == 0) >= 1:
                raise ValueError('Evklid metrikasida nominal alomatlar bo\'lishi mumkin emas.')
            data = self.normal_data
            m = self.m
            distance_matrix = np.zeros((m, m))
            for i in range(m):
                distance_matrix[i] = np.sum((data[i] - data)**2, axis=1)
            return distance_matrix
        except ValueError as e:
            print('Xatolik:', e)  

    def distanceMatrixChebyshev(self):
        characteristic_vector = self.characteristic_vector
        try:
            if np.sum(characteristic_vector == 0) >= 1:
                raise ValueError('Chebyshev metrikasida nominal alomatlar bo\'lishi mumkin emas.')
            data = self.normal_data
            m = self.m
            distance_matrix = np.zeros((m, m))
            for i in range(m):
                distance_matrix[i] = np.max(np.abs(data[i] - data), axis=1)
            return distance_matrix
        except ValueError as e:
            print('Xatolik:', e) 
    
    def distanceMatrixJuravlov(self):
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

# SINF TARIFI
# Sinfga 3 ta parametr keladi. 1 - berilganlar, 2 - matrika turi, 3 - normalizatsiya

# Berilganlarga quyidagi standart ko'rinishida kelishi kerak:
# 1. Obyektlar kesishmaydigan va takrorlanmaydigan
# 2. Tushirib qoldirilgan alomat bironta ham obyektda uchramaydi
# 3. Berilganlar o'qituvchisiz(unlabled) bo'lishi
# 4. Harakteristik vektor mavjud va unda 0 - nominal, 1 - miqdoriy bo'lishi
# 5. Agar turli tipdagi berilganlar bo'lsa, metrika 'juravlov' bo'lishi