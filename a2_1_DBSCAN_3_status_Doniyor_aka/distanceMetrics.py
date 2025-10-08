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
            self.distance_matrix = self.distanceMatrixEuclidean()
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
                    re_data[i, j] = np.round(2 * (data[i, j] - by_col_min) / denomirator - 1, 5)
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
                for j in range(i+1, m):
                    delta_num = np.linalg.norm(data[i] - data[j])
                    distance_matrix[i, j] = delta_num
                    distance_matrix[j, i] = delta_num
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
                for j in range(i+1, m):
                    delta_num = np.max(np.abs(data[i] - data[j]))
                    distance_matrix[i, j] = delta_num
                    distance_matrix[j, i] = delta_num
            return distance_matrix
        except ValueError as e:
            print('Xatolik:', e) 
    
    def distanceMatrixJuravlov(self):
        characteristic_vector = self.characteristic_vector
        data = self.normal_data
        m = self.m
        distance_matrix = np.zeros((m, m))
        for i in range(m):
            for j in range(i+1, m):
                delta_nominal = 0
                delta_quantitative = 0
                for col in range(len(characteristic_vector)):
                    if characteristic_vector[col] == 1:
                        delta_quantitative += np.abs(data[i, col] - data[j, col])
                    elif characteristic_vector[col] == 0:
                        if data[i, col] != data[j, col]:
                            delta_nominal += 1
                delta_num = delta_quantitative + delta_nominal  
                
                distance_matrix[i, j] = delta_num
                distance_matrix[j, i] = delta_num
        return distance_matrix   

# SINF TARIFI
# Ushbu sinfga berilganlar uzatilganda sinf obyektlar soni va ular orasidagi masofani hisoblaydi
# Sinfga 3 ta parametr keladi. 1 - berilganlar, 2 - matrika turi, 3 - normalizatsiya

# Berilganlarga quyidagi standart ko'rinishida kelishi kerak:
# 1. Obyektlar kesishmaydigan va takrorlanmaydigan
# 2. Tushirib qoldirilgan alomat bironta ham obyektda uchramaydi
# 3. Berilganlar o'qituvchisiz(unlabled) bo'lishi
# 4. Agar turli tipdagi berilganlar bo'lsa, eng oxirgi satrda harakteristik vektor mavjud va unda 0 - nominal, 1 - miqdoriy
# 5. Agar turli tipdagi berilganlar bo'lsa, metrika 'juravlov' bo'lishi