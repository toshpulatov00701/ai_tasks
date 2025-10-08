import numpy as np
import math
import distanceMetrics
import myRelFun
import anomDetHyperSpere
from datetime import datetime

class myDBSCAN:
    distance_matrix = None
    n = None                        # k = 2, 3, 4, ... n
    lambda_min_max = None           # Tuple. 0 - min, 1 - max. Barcha k lar uchun umumiy lambda min va max. 
    e_avarages_K = None             # k lar bo'yicha e
    m = None                        # obyektlar soni
    f = 3                           # 3 xona aniqlikda
    def __init__(self, data, n, metric_type, normal_type=None):
        self.n = n
        objDistanceMetrics = distanceMetrics.dMetrics(data, metric_type, normal_type)
        self.m = objDistanceMetrics.m
        self.distance_matrix = np.sort(objDistanceMetrics.distance_matrix)
        self.setBoundaries()

    def setBoundaries(self):
        distance_matrix = self.distance_matrix
        m = self.m
        n = self.n
        f = self.f
        e_avarages_K = np.average(distance_matrix, axis=0)
        e_avarages_K = e_avarages_K[2:n+1]                                       # {2, 3, 4, 5, .... } uchun e qiymatlari 
        lambda_min_array = np.zeros(n - 1)
        lambda_max_array = np.zeros(n - 1)

        for i in range(n - 1): 
            def recursionlambdaMin(lambda_min_1, lambda_min_2):                  # Rekursiv holatda lambda_min ni topish. Farqi 0.001 bo'lguncha izla             
                objL1C = self.setStatus(e_avarages_K * lambda_min_1)
                if round(lambda_min_1, f) == round(lambda_min_2, f) and (np.sum(objL1C[:,i] == 2)):             # lambda_min_1 va lambda_min_2 verguldan keyingi f ta raqami bir xil bo'lguncha davom et
                    return math.floor(lambda_min_1 * (10**f))/(10**f)
                lambda_min = (lambda_min_1 + lambda_min_2) / 2.0
                obj_status = self.setStatus(e_avarages_K * lambda_min)
                count_anomolouses = np.sum(obj_status[:,i] == 2)
                if count_anomolouses == m:
                    return recursionlambdaMin(lambda_min, lambda_min_2)
                else:
                    return recursionlambdaMin(lambda_min_1, lambda_min)

            def recursionlambdaMax(lambda_max_1, lambda_max_2):                  # Rekursiv holatda lambda_max ni topish. Farqi 0.001 bo'lguncha izla
                if round(lambda_max_1, f) == round(lambda_max_2, f):             # lambda_min_1 va lambda_min_2 verguldan keyingi 4 ta raqami bir xil bo'lguncha davom et
                    return math.ceil(lambda_max_2 * (10**f))/(10**f)     
                lambda_max = (lambda_max_1 + lambda_max_2) / 2.0
                obj_status = self.setStatus(e_avarages_K * lambda_max)
                obj_status_2 = self.setStatus(e_avarages_K * lambda_max_2)
                count_anomolouses = np.sum(obj_status[:,i] == 2)
                if count_anomolouses == 0:
                    return recursionlambdaMax(lambda_max_1, lambda_max)
                elif np.sum(obj_status_2[:,i] == 2) == 0:
                    return recursionlambdaMax(lambda_max, lambda_max_2)
                else:
                    return recursionlambdaMax(lambda_max_2, lambda_max_2 + lambda_max_1)
            lambda_min_array[i] = recursionlambdaMin(0, 1)
            lambda_max_array[i] = recursionlambdaMax(1, 2)
            # print(lambda_min_array[i], lambda_max_array[i])
        self.lambda_min_max = np.max(lambda_min_array), np.min(lambda_max_array)   # umumiy lambda_min - barcha k lar bo'yicha minimumlar ichindan max. 
        # print('ortacha e:', e_avarages_K)
        # print('umimiy:', self.lambda_min_max)
        self.e_avarages_K = e_avarages_K

    # def setStatus(self, e_everages):
    #     m = self.m
    #     distance_matrix = self.distance_matrix
    #     length_e = len(e_everages)
    #     data_status = np.zeros((m, length_e), dtype=int)
    #     for i in range(m):
    #         for j in range(length_e):
    #             if np.sum(distance_matrix[i] < e_everages[j]) - 1 >= j + 2:  # j + 2 - indexda k=j + 2 bo'lgandagi qiymati, -1 o'zini chiqarib ketish
    #                 data_status[i, j] = 1                                    # 1 - yadroviy
    #             elif np.sum(distance_matrix[i] < e_everages[j])-1 == 0:
    #                 data_status[i, j] = 3                                    # 3 - anomal
    #             else:
    #                 data_status[i, j] = 2                                    # 2 - chegaraviy
    #     return data_status
    
    def setStatus(self, e_everages):
        m = self.m
        distance_matrix = self.distance_matrix
        length_e = len(e_everages)
        data_status = np.zeros((m, length_e), dtype=int)
        for i in range(m):
            for j in range(length_e):
                if np.sum(distance_matrix[i] < e_everages[j]) - 1 >= j + 2:  # j + 2 - indexda k=j + 2 bo'lgandagi qiymati, -1 o'zini chiqarib ketish
                    data_status[i, j] = 1                                    # 1 - yadroviy
                elif np.sum(distance_matrix[i] < e_everages[j])-1 == 0:
                    data_status[i, j] = 2                                    # 2 - anomal
                else:
                    data_status[i, j] = 1                                    # 1 - chegaraviy
        return data_status
    
    def buildArtificialData(self, e_1, e_2):                                     # 2, 3, 4, ...  holatlar uchun e hisoblash. l - bo'laklar soni
        e_avarages_K = self.e_avarages_K
        m = self.m
        K1_class = np.ones((m, 1), dtype=int)
        K1_data = np.hstack((self.setStatus(e_avarages_K * e_1), K1_class)) # Birinchi sinfni tashkil etish
        K2_class = np.ones((m, 1), dtype=int) * 2
        K2_data = np.hstack((self.setStatus(e_avarages_K * e_2), K2_class)) # Ikkinchi sinfni tashkil etish
        new_data = np.vstack((K1_data, K2_data))
        return new_data

    def possibleLambdaes(self):                                      #  mumkin bo'lgan lamdalar.
        lambda_min = self.lambda_min_max[0]
        lambda_max = self.lambda_min_max[1]
        e_avarages_K = self.e_avarages_K
        possible_lambdaes = []
        f = self.f
        start = datetime.now()
        with open('datasets/possibleLambdaes.txt', 'w') as ff:       # faylni tozalab olish
            pass
        while(True):
            def recursionLambda(minmum, maxmum):
                objL1C = self.setStatus(e_avarages_K * minmum)
                objL2C = self.setStatus(e_avarages_K * maxmum)
                lambda_delta = (minmum + maxmum) / 2.0
                if (round(minmum, f) == round(maxmum, f)) and (np.sum(objL1C != objL2C) >= 1):
                    return math.ceil(maxmum * (10**f))/(10**f)
                elif np.sum(objL1C != objL2C) == 0:
                    return recursionLambda(lambda_delta, maxmum + (maxmum - minmum))
                return recursionLambda(minmum, lambda_delta)
            
            res = recursionLambda(lambda_min, lambda_max)
            with open('datasets/possibleLambdaes.txt', 'a') as ff:
                ff.write(str(res) + '\n')
            possible_lambdaes.append(res)
            lambda_min = res
            if res == lambda_max:
                break
        end = datetime.now()
        self.buildStabilityData()
        print('Duration time ==> ', end - start)
        return possible_lambdaes
    
    def buildStabilityData(self):                                                 # Tug'unliklar asosida qurilgan yangi dataset
        pos_lambdaes = np.loadtxt('datasets/possibleLambdaes.txt', dtype=float)
        with open('datasets/stabilitesData.txt', 'w') as ff:                      # faylni tozalab olish
            pass
        for i in range(0, len(pos_lambdaes)):
            artificial_data = self.setStatus(self.e_avarages_K * pos_lambdaes[i])
            objRelFun = myRelFun.relatedFunction(artificial_data)
            stabilites = objRelFun.stabilityFeatures()
            stabilites = np.append(stabilites, pos_lambdaes[i])
            with open("datasets/stabilitesData.txt", "a") as ff:
                np.savetxt(ff, stabilites.reshape(1, -1), fmt="%g", delimiter=' ')
        self.findOptimalLambda()
    
    def findOptimalLambda(self):                   # Gipershar yordamida optimal lambdani topish
        stb_data = np.loadtxt('datasets/stabilitesData.txt', dtype=float)
        objFindAnom = anomDetHyperSpere.buildHyperSpere(stb_data)
        objFindAnom.findHyperspere()
        print('Optimal lambda: ', stb_data[objFindAnom.centerObjIndex(),-1])
        return stb_data[objFindAnom.centerObjIndex(),-1]