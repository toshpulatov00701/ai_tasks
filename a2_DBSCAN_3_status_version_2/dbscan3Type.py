import numpy as np
import math
from distanceMetrics import dMetrics
from myRelFun import relatedFunction
import anomDetHyperSpere
from datetime import datetime
from myDBSCAN import ClassicDBSCAN

class DBSCAN3Type(dMetrics):
    n = None                        # k = 2, 3, 4, ... n
    lambda_min_max = None           # Tuple. 0 - min, 1 - max. Barcha k lar uchun umumiy lambda min va max. 
    e_avarages_K = None             # k lar bo'yicha e
    f = 3                           # 3 xona aniqlikda
    data = None                     # Dastlabki data
    metric_type = None
    normal_type = None
    
    def __init__(self, data, n, metric_type, normal_type=None):
        self.data = data
        self.n = n
        self.metric_type = metric_type
        self.normal_type = normal_type
        super().__init__(data, metric_type, normal_type)
        self.setBoundaries()

    def setBoundaries(self): 
        distance_matrix = np.sort(self.distance_matrix)
        n = self.n
        f = self.f
        min_dist = np.min(distance_matrix[distance_matrix != 0])
        e_avarages_K = np.average(distance_matrix, axis=0)
                
        if self.metric_type == 'euclidean':
            e_avarages_K = np.sqrt(e_avarages_K[2:n+1])                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min_array = np.sqrt(min_dist) / e_avarages_K                      
            center_d_max = self.findMaxByCenter()
            lambda_max_array = np.sqrt(center_d_max) / e_avarages_K
        else:
            e_avarages_K = e_avarages_K[2:n+1]                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min_array = min_dist / e_avarages_K                     
            center_d_max = self.findMaxByCenter()
            lambda_max_array = center_d_max / e_avarages_K
        print('lambda_min_array:', lambda_min_array)
        print('lambda_max_array:', lambda_max_array)
        print('e_avarages_K: ', e_avarages_K)
        self.lambda_min_max = np.round(np.max(lambda_min_array), f), np.round(np.min(lambda_max_array), f)  # umumiy lambda_min - barcha k lar bo'yicha minimumlar ichindan max. 
        self.e_avarages_K = e_avarages_K
    
    def findExtrimums(self):
        e_avarages_K = self.e_avarages_K
        ekstirmum_lambdaes = np.ones(len(e_avarages_K)) * (-1)
        for i in range(len(e_avarages_K)):
            a = self.lambda_min_max[0]
            b = self.lambda_min_max[1]
            gr = (np.sqrt(5) - 1) / 2
            r = e_avarages_K[i]
            k = i + 2      
            while np.abs(a - b) > 1 / (10**self.f):
                print('a, b: ', a, b)
                d_gr = gr * (b - a)
                x1 = b - d_gr
                x2 = a + d_gr
                db = ClassicDBSCAN(self.data, eps = r * x1, min_samples = k, metric_type=self.metric_type, normal_type=self.normal_type)
                objRelFun = relatedFunction(db.getStatuses())
                f_x1 = objRelFun.stabilityFeatures()
                
                db = ClassicDBSCAN(self.data, eps = r * x2, min_samples = k, metric_type=self.metric_type, normal_type=self.normal_type)
                objRelFun = relatedFunction(db.getStatuses())
                f_x2 = objRelFun.stabilityFeatures()
                if f_x1 > f_x2:
                    a = x1
                else:
                    b = x2
            ekstirmum_lambdaes[i] = (a + b) / 2
        return ekstirmum_lambdaes
    
    def setStatus(self, e_everages):
        m = self.m
        length_e = len(e_everages)
        data_status = np.zeros((m, length_e), dtype=int)
        for i_e in range(length_e):
            db = ClassicDBSCAN(self.data, eps=e_everages[i_e], min_samples=i_e + 2, metric_type=self.metric_type, normal_type=self.normal_type)
            data_status[:,i_e] = db.getStatuses()
        return data_status    