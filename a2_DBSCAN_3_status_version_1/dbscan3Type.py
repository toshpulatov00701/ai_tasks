import numpy as np
import math
from distanceMetrics import dMetrics
from myRelFun import relatedFunction
import anomDetHyperSpere
from datetime import datetime
from sklearn.cluster import DBSCAN
from myDBSCAN import ClassicDBSCAN

class DBSCAN3Type(dMetrics):
    n = None                        # k = 2, 3, 4, ... n
    lambda_min_max = None           # Tuple. 0 - min, 1 - max. Barcha k lar uchun umumiy lambda min va max. 
    e_avarages_K = None             # k lar bo'yicha e
    f = 3                           # 3 xona aniqlikda
    data = None                     # Normalizatsiyadan keyingi data
    metric_type = None
    normal_type = None
    
    def __init__(self, data, n, metric_type, normal_type=None):
        self.data = data
        self.n = n
        self.metric_type = metric_type
        self.normal_type = normal_type
        super().__init__(data, metric_type, normal_type)
        self.setBoundaries()

    def setBoundaries(self):  # Max chegaradan sezilari darajada kichik qiymatlarda ham javob bor. Katta datasetlarda muommolar bo'ladi.
        distance_matrix = np.sort(self.distance_matrix)
        n = self.n
        f = self.f
        min_dist = np.min(distance_matrix[distance_matrix != 0])
        max_dist = np.max(distance_matrix)
        e_avarages_K = np.average(distance_matrix, axis=0)
        
        if self.metric_type == 'euclidean':
            e_avarages_K = np.sqrt(e_avarages_K[2:n+1])                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min_array = np.sqrt(min_dist) / e_avarages_K                      
            lambda_max_array = np.sqrt(max_dist) / e_avarages_K
        else:
            e_avarages_K = e_avarages_K[2:n+1]                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
            lambda_min_array = min_dist / e_avarages_K                      
            lambda_max_array = max_dist / e_avarages_K
        print('lambda_min_array:', lambda_min_array)
        print('lambda_max_array:', lambda_max_array)
        print('e_avarages_K: ', e_avarages_K)
        self.lambda_min_max = np.round(np.max(lambda_min_array), f), np.round(np.min(lambda_max_array), f)  # umumiy lambda_min - barcha k lar bo'yicha minimumlar ichindan max. 
        self.e_avarages_K = e_avarages_K
    
    def setStatus(self, e_everages):   # Aralash fazo bo'lganda. Juravlov
        m = self.m
        length_e = len(e_everages)
        data_status = np.zeros((m, length_e), dtype=int)
        for i_e in range(length_e):
            db = ClassicDBSCAN(self.data, eps=e_everages[i_e], min_samples=i_e + 2, metric_type=self.metric_type, normal_type=self.normal_type)
            data_status[:,i_e] = db.getStatuses()
        return data_status
    
    def buildArtificialData(self, e_1, e_2):                                # 2, 3, 4, ...  holatlar uchun e hisoblash. l - bo'laklar soni
        e_avarages_K = self.e_avarages_K
        m = self.m
        K1_class = np.ones((m, 1), dtype=int)
        K1_data = np.hstack((self.setStatus(e_avarages_K * e_1), K1_class)) # Birinchi sinfni tashkil etish
        K2_class = np.ones((m, 1), dtype=int) * 2
        K2_data = np.hstack((self.setStatus(e_avarages_K * e_2), K2_class)) # Ikkinchi sinfni tashkil etish
        new_data = np.vstack((K1_data, K2_data))
        return new_data

    # def findExtrimums(self):     # To'plam(sinf)lari o'zaro kesishmaydigan barcha lambdalarni hisoblamasdan ekstimum(minimum)ni topish. Golden-section search.
    #     e_avarages_K = self.e_avarages_K
    #     res_lambdaes = np.ones(len(e_avarages_K)) * (-1)
    #     for i in range(len(e_avarages_K)):
    #         a = self.lambda_min_max[0]
    #         b = self.lambda_min_max[1]
    #         gr = (np.sqrt(5) - 1) / 2
    #         r = e_avarages_K[i]
    #         k = i + 2      
    #         while np.abs(a - b) > 1 / (10**self.f):
    #             d_gr = gr * (b - a)
    #             x1 = b - d_gr
    #             x2 = a + d_gr
    #             db = ClassicDBSCAN(self.data, eps = r * x1, min_samples = k, metric_type=self.metric_type, normal_type=self.normal_type)
    #             objRelFun = relatedFunction(db.getStatuses())
    #             f_x1 = objRelFun.stabilityFeatures()
                
    #             db = ClassicDBSCAN(self.data, eps = r * x2, min_samples = k, metric_type=self.metric_type, normal_type=self.normal_type)
    #             objRelFun = relatedFunction(db.getStatuses())
    #             f_x2 = objRelFun.stabilityFeatures()
    #             if f_x1 > f_x2:
    #                 a = x1
    #             else:
    #                 b = x2
    #         res_lambdaes[i] = (a + b) / 2
    #     return res_lambdaes

    def possibleLambdaes(self):                                             # mumkin bo'lgan lamdalar.
        lambda_min = self.lambda_min_max[0]
        lambda_max = self.lambda_min_max[1]
        e_avarages_K = self.e_avarages_K
        possible_lambdaes = []
        f = self.f
        start = datetime.now()
        with open('datasets/possibleLambdaes.txt', 'w') as ff:       # Faylni tozalab olish
            pass
        while(True):
            def recursionLambda(minmum, maxmum):
                objL1C = self.setStatus(e_avarages_K * minmum)
                objL2C = self.setStatus(e_avarages_K * maxmum)
                lambda_delta = (minmum + maxmum) / 2.0
                if (round(minmum, f) == round(maxmum, f)) and (np.sum(objL1C != objL2C) >= 1):
                    return math.ceil(maxmum * (10**f))/(10**f)       # Kattasiga qarab yaxlitlash
                elif np.sum(objL1C != objL2C) == 0:
                    return recursionLambda(lambda_delta, maxmum + (maxmum - minmum))
                return recursionLambda(minmum, lambda_delta)
            
            res = recursionLambda(lambda_min, lambda_max)
            with open('datasets/possibleLambdaes.txt', 'a') as ff:
                ff.write(str(res) + '\n')
            possible_lambdaes.append(res)
            lambda_min = res
            if np.sum(self.setStatus(e_avarages_K * res) == 3) == 0:    # Oxirida barcha obyektlar bitta klasterga tegishli bo'lib qoladi
                break
        end = datetime.now()
        self.buildStabilityData()
        print('Duration time ==> ', end - start)
        return possible_lambdaes
    
    def buildStabilityData(self):                                                 # Tug'unliklar asosida qurilgan yangi dataset
        pos_lambdaes = np.loadtxt('datasets/possibleLambdaes.txt', dtype=float)
        with open('datasets/stabilitesData.txt', 'w') as ff:                      # Faylni tozalab olish
            pass
        for i in range(0, len(pos_lambdaes)):
            artificial_data = self.setStatus(self.e_avarages_K * pos_lambdaes[i])
            objRelFun = relatedFunction(artificial_data)
            stabilites = objRelFun.stabilityFeatures()
            stabilites = np.append(stabilites, pos_lambdaes[i])
            with open("datasets/stabilitesData.txt", "a") as ff:
                np.savetxt(ff, stabilites.reshape(1, -1), fmt="%g", delimiter=' ')
    
    def findOptimalLambda(self):                   # Gipershar yordamida optimal lambdani topish
        stb_data = np.loadtxt('datasets/stabilitesData.txt', dtype=float)
        objFindAnom = anomDetHyperSpere.buildHyperSpere(stb_data)
        objFindAnom.findHyperspere()
        print('Optimal lambda: ', stb_data[objFindAnom.centerObjIndex(),-1])
        return stb_data[objFindAnom.centerObjIndex(),-1]