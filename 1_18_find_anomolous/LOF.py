import numpy as np
import matplotlib.pyplot as plt
import EstALg

class LOF:
    data = None
    distances_matrix = None
    
    def __init__(self, data):
        self.data = data
        self.setDistancesMatrix()
    
    def setDistancesMatrix(self):
        data = self.data
        rows, cols = np.shape(data)
        distances = np.zeros((rows, rows))
        for i in range(rows):
            for j in range(i, rows):
                d = np.linalg.norm(data[i] - data[j], axis=0)
                distances[i, j] = d
                distances[j, i] = d
        self.distances_matrix = distances
    
    def colculate_RDk(self, S_u_index, S_v_index, k):         # S_v dan S_u ga erishiluvchi masofa
        distance_matrix = self.distances_matrix
        k_dis = np.sort(distance_matrix[S_v_index])[k + 1]    # S_v ga eng yaqin k obyektigacha bo'lgan masofa
        d = distance_matrix[S_v_index, S_u_index]             # S_u va S_v obyektlar o'rtasidagi masofa
        if k_dis > d: return k_dis
        return d

    def colculate_lrd(self, S_u_index, k):
        distance_matrix = self.distances_matrix
        S_v_indexes = np.argsort(distance_matrix[S_u_index])[1:k+1]   # S_u obyektga eng yaqin bo'lgan k ta obyekt indekslari
        sum_RDk = 0
        for S_v_index in S_v_indexes:
            sum_RDk += self.colculate_RDk(S_u_index, S_v_index, k)
        return 1 / (sum_RDk / k)

    def colculate_LOFk(self, S_u_index, k):
        distance_matrix = self.distances_matrix
        S_v_indexes = np.argsort(distance_matrix[S_u_index])[1:k+1]   # S_u obyektga eng yaqin bo'lgan k ta obyekt indekslari
        sum_lrd = 0
        for S_v_index in S_v_indexes:
            sum_lrd += self.colculate_lrd(S_v_index, k)
        lof_k = (sum_lrd / k) / self.colculate_lrd(S_u_index, k)
        return lof_k

    def findAnomalouses(self, k, threshold):
        data = self.data
        rows, _ = np.shape(data)
        objs_LOF = np.zeros(rows)
        for item_index in range(rows):
            objs_LOF[item_index] = self.colculate_LOFk(item_index, k)
        
        obj_anomoluses = (objs_LOF > threshold).astype(int)
        obj_anomoluses[obj_anomoluses == 1] = -1
        obj_anomoluses[obj_anomoluses == 0] = 1
        return obj_anomoluses
    
    def findCloserThreshold(self, real_labels):                    # thresholdni hisoblash.        
        def recursionFindThreshold(min_threshold, max_threshold):
            ress = np.zeros((11, 2))
            delta = np.abs((min_threshold - max_threshold) / 10)
            for i in range(0, 11):
                threshold = min_threshold + i * delta
                obj_anomoluses = self.findAnomalouses(20, threshold)
                est_alg = EstALg.EstimationAlgorithm(real_labels, obj_anomoluses)
                ress[i, 0] = threshold
                ress[i, 1] = est_alg.f1_score                       # Qaysi aniqlik kerak bo'lsa, shunisi tanlanadi. accuracy, precision, recall, f1_score
            if len(np.unique(ress[:,1])) == 1:
                return threshold
            sorted_ress = ress[np.argsort(ress[:,1])]
            min_threshold = np.min([sorted_ress[-2,0], sorted_ress[-1,0]])
            max_threshold = np.max([sorted_ress[-2,0], sorted_ress[-1,0]])
            return recursionFindThreshold(min_threshold, max_threshold)
        
        closer_theshold = recursionFindThreshold(1, 10)
        print(closer_theshold)

data = np.loadtxt('datasets/testdata4.txt')
X_data = data[:,:-1]
y_data = data[:,-1]   # Aniq javoblar. Anomal yoki normal ekanligi

obj = LOF(X_data)

# obj.findCloserThreshold(y_data)

res_est = EstALg.EstimationAlgorithm(y_data, obj.findAnomalouses(20, 2.98), -1)
res_est.showAllParametr()

# Algoritm ishlashida oldiniga thresholdni hisoblab olib, chiqqan natijani anomallarni topish uchun ishlatiladi.