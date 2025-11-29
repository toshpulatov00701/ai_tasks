import numpy as np
from distance_metrics import DistMetrics
from relation_function import RelatedFunction
from myDBSCAN import ClassicDBSCAN

class DBSCAN3Type(DistMetrics):
    # lambda_min_max - Tuple. 0 - min, 1 - max
    # e_avarage - k bo'yicha o'rtacha e
        
    def __init__(self, data, k, metric_type, normal_type=None):
        self.data = data            # Normalizatsiyasiz dastlabki data
        self.k = k                  # Qo'shnilar soni
        super().__init__(data, metric_type, normal_type)
        self.set_boundaries()

    def set_boundaries(self): 
        distance_matrix = np.sort(self.distance_matrix)
        k = self.k
        min_dist = np.min(distance_matrix[distance_matrix != 0])
        max_dist = np.max(distance_matrix[:, k])                              # Eng yaqin k qo'shnilari orasidan eng kattasi
        
        if self.metric_type == 'euclidean':
            e_avarages_K = np.average(np.sqrt(distance_matrix), axis=0)
            e_avarage = e_avarages_K[k]                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min = np.sqrt(min_dist) / e_avarage
            lambda_max = np.sqrt(max_dist) / e_avarage
        else:
            e_avarages_K = np.average(distance_matrix, axis=0)
            e_avarage = e_avarages_K[k]                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min = min_dist / e_avarage
            lambda_max = max_dist / e_avarage

        print('lambda_min:', lambda_min)
        print('lambda_max:', lambda_max)
        print('o\'rtacha radius: ', e_avarage)
        self.lambda_min_max = lambda_min, lambda_max
        self.e_avarage = e_avarage
    
    def find_extrimums(self, anomal_percent, number_parts):
        l_min, l_max = self.lambda_min_max
        e_avarage = self.e_avarage
        d = (l_max - l_min) / number_parts
        def f(delta_lambda):
            db = ClassicDBSCAN(self.data, eps = e_avarage * delta_lambda, min_samples = self.k, metric_type=self.metric_type, normal_type=self.normal_type)    
            objRelFun = RelatedFunction(db.get_statuses(), anomal_percent)
            return objRelFun.stability_features()
        
        l_1 = l_min + 0 * d
        f_1 = f(l_1)
        l_2 = l_min + 1 * d
        f_2 = f(l_2)
        i_start = 0
        if f_1 <= f_2:
            for i in range(2, number_parts + 1):
                l_start = l_min + i * d
                f_start = f(l_start)
                if f_start >= f_2:
                    f_2 = f_start
                else:
                    i_start = i
                    break
        a, b = l_min, l_max
        f_1, f_2, f_3 = 1, 2, 3
        for i in range(i_start, number_parts + 1):
            l_1 = l_min + i * d
            f_1 = f(l_1)
            
            while True:
                i = i + 1
                l_2 = l_min + (i) * d
                f_2 = f(l_2)
                if f_2 != f_1:
                    break

            while True:
                i = i + 1
                l_3 = l_min + (i) * d
                f_3 = f(l_3)
                if f_3 != f_2:
                    # i = i - 1
                    break
            
            if f_2 < f_1 and f_2 < f_3:
                a, b = l_1, l_3
                break
        
        # Golden Selection Search usuli asosida
        gr = (np.sqrt(5) - 1) / 2
        while np.abs(a - b) > 0.001:
            d_gr = gr * (b - a)
            x1 = b - d_gr
            x2 = a + d_gr
            f_x1 = f(x1)
            f_x2 = f(x2)
            if f_x1 > f_x2:
                a = x1
            else:
                b = x2
        print('lambda(ekstrimum):',(a + b) / 2)
        res_lambda = (a + b) / 2
        return res_lambda


# data = np.loadtxt('datasets/testdata2.txt', dtype=float)
# metric_type='euclidean'
# normal_type='normalization'
# k = 4
# anom_percent = 50
# objDb = DBSCAN3Type(data, k=k, metric_type=metric_type, normal_type=normal_type)
# eks = objDb.find_extrimums(anom_percent, 500)
# r = objDb.e_avarage * eks
# db = ClassicDBSCAN(data, eps=r, min_samples=k, metric_type=metric_type, normal_type=normal_type)
# clasters_name = np.unique_all(db.c_labels).values
# print('clasters_name:', clasters_name)
# db_status = db.get_statuses3()
# print(f'Anomallar soni: {np.sum(db_status == 3)}')
# print(f'Anomallar %: {np.sum(db_status == 3) * 100 / len(data[:-1,:])}')