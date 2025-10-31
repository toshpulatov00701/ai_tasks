import numpy as np
import math
from distanceMetrics import dMetrics
from myRelFun import relatedFunction
import anomDetHyperSpere
from datetime import datetime
from myDBSCAN import ClassicDBSCAN

class DBSCAN3Type(dMetrics):
    k = None                        # k = 2, 3, 4, ... n
    lambda_min_max = None           # Tuple. 0 - min, 1 - max. Barcha k lar uchun umumiy lambda min va max. 
    e_avarage = None                # k bo'yicha e
    f = 3                           # 3 xona aniqlikda
    data = None                     # Normalizatsiyadan keyingi data
    metric_type = None
    normal_type = None
    
    def __init__(self, data, k, metric_type, normal_type=None):
        self.data = data
        self.k = k
        self.metric_type = metric_type
        self.normal_type = normal_type
        super().__init__(data, metric_type, normal_type)
        self.setBoundaries()

    def setBoundaries(self): 
        distance_matrix = np.sort(self.distance_matrix)
        k = self.k
        f = self.f
        min_dist = np.min(distance_matrix[distance_matrix != 0])
        e_avarages_K = np.average(distance_matrix, axis=0)
        
        if self.metric_type == 'euclidean':
            e_avarage = np.sqrt(e_avarages_K[k])                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min_array = np.sqrt(min_dist) / e_avarage                      
        else:
            e_avarage = e_avarages_K[k]                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min_array = min_dist / e_avarage                      
        
        def recursionlambdaMax(lambda_max_1, lambda_max_2):                  # Rekursiv holatda lambda_max ni topish. Farqi 0.001 bo'lguncha izla
            print(lambda_max_1, lambda_max_2)
            if np.abs(lambda_max_2 - lambda_max_1) < 0.1:                    # lambda_min_1 va lambda_min_2 verguldan keyingi 4 ta raqami bir xil bo'lguncha davom et
                return lambda_max_2
            lambda_avg = (lambda_max_1 + lambda_max_2) / 2
            
            db = ClassicDBSCAN(self.data, eps=e_avarage * lambda_avg, min_samples=k, metric_type=self.metric_type, normal_type=self.normal_type)
            obj_status_avg = db.getStatuses3()

            db = ClassicDBSCAN(self.data, eps=e_avarage * lambda_max_2, min_samples=k, metric_type=self.metric_type, normal_type=self.normal_type)
            obj_status_2 = db.getStatuses3()
            
            if np.sum(obj_status_avg == 3) == 0:
                return recursionlambdaMax(lambda_max_1, lambda_avg)
            elif np.sum(obj_status_2 == 3) == 0:
                return recursionlambdaMax(lambda_avg, lambda_max_2)
            else:
                return recursionlambdaMax(lambda_max_2, lambda_max_2 + lambda_max_1)
        lambda_max_array = recursionlambdaMax(1, 2)

        print('lambda_min_array:', lambda_min_array)
        print('lambda_max_array:', lambda_max_array)
        print('e_avarage: ', e_avarage)
        self.lambda_min_max = np.round(np.max(lambda_min_array), f), np.round(np.min(lambda_max_array), f)  # umumiy lambda_min - barcha k lar bo'yicha minimumlar ichindan max. 
        self.e_avarage = e_avarage
    
    def findExtrimums(self, anomal_percent):
        e_avarage = self.e_avarage
        k = self.k
        res_lambda = -1
        a = self.lambda_min_max[0]
        b = self.lambda_min_max[1]
        gr = (np.sqrt(5) - 1) / 2
        r = e_avarage
          
        while np.abs(a - b) > 1 / (10**self.f):
            print(a, b)
            d_gr = gr * (b - a)
            x1 = b - d_gr
            x2 = a + d_gr
            db = ClassicDBSCAN(self.data, eps = r * x1, min_samples = k, metric_type=self.metric_type, normal_type=self.normal_type)
            objRelFun = relatedFunction(db.getStatuses(), anomal_percent)
            f_x1 = objRelFun.stabilityFeatures()
            
            db = ClassicDBSCAN(self.data, eps = r * x2, min_samples = k, metric_type=self.metric_type, normal_type=self.normal_type)
            objRelFun = relatedFunction(db.getStatuses(), anomal_percent)
            f_x2 = objRelFun.stabilityFeatures()
            if f_x1 > f_x2:
                a = x1
            else:
                b = x2
        print('resssss:',(a + b) / 2)
        res_lambda = (a + b) / 2
        return res_lambda


########################################









    # def findExtrimums(self, anomal_percent):
        
    #     e_avarages_K = self.e_avarages_K
        
    #     # print('Minmax: ', lambda_min, lambda_max)
    #     for i in range(len(e_avarages_K)):
    #         r = e_avarages_K[i]
    #         k = i + 2
    #         # ppp = 0
    #         lambda_min = self.lambda_min_max[0]
    #         lambda_max = self.lambda_min_max[1]
    #         while(np.abs(lambda_max - lambda_min) > 0.01):
    #             print('Boshidagi:', lambda_min, lambda_max)
    #             # ppp+=1
    #             d = np.abs(lambda_max - lambda_min) / 10
    #             stb_by_lambda = np.ones((2, 11)) * (-1)
    #             print('d=', d)
    #             for j in range(11):
    #                 lambda_delta = lambda_min + d * j
    #                 # print(lambda_delta)
    #                 db = ClassicDBSCAN(self.data, eps = r * lambda_delta, min_samples = k, metric_type=self.metric_type, normal_type=self.normal_type)
    #                 objRelFun = relatedFunction(db.getStatuses(), anomal_percent)
    #                 stb_by_lambda[0 ,j] = np.round(objRelFun.stabilityFeatures(), 8)
    #                 stb_by_lambda[1 ,j] = lambda_delta
                
    #             print(stb_by_lambda)
    #             _, counts = np.unique(stb_by_lambda[0,:], return_counts=True)
    #             # print(counts)
    #             if counts[0] == 10 or counts[0] == 11: # 
    #                 break
    #             else:
    #                 min_1 = np.min(stb_by_lambda[0,:])
    #                 min_2 = np.min(stb_by_lambda[0,stb_by_lambda[0,:]!= min_1])
    #                 index_min_1 = np.where(stb_by_lambda[0,:] == min_1)[0][0]
    #                 index_min_2 = np.where(stb_by_lambda[0,:] == min_2)[0][0]
    #                 lambda_min = stb_by_lambda[1,index_min_1]
    #                 lambda_max = stb_by_lambda[1,index_min_2]
    #                 # print(stb_by_lambda)
    #                 # print('Oxirida:', lambda_min, lambda_max)
    #                 # print('min_1, min_2:', min_1, min_2)
    #                 # print('index_min_1, index_min_2:', index_min_1, index_min_2)
    #                 # print('---------------------')
    #             # if ppp == 10:
    #             #     break
    #         res_lambda = np.round((lambda_max + lambda_min) / 2, 5)
    #         print(f'k={k} uchun javob: ', res_lambda)
            
# data = np.loadtxt('datasets/ionosphere.txt', dtype=float)
# n = 6  # 2, 3, 4...n
# objDb = DBSCAN3Type(data, n, metric_type='euclidean', normal_type='normalization')
# print(objDb.findExtrimums(anomal_percent=20))