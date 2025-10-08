import numpy as np

class buildHyperSpere:
    
    real_data = None     # Data'ning harakteristik vektordan tozalangan holati
    C = None             # Markaz
    r = None             # Gipershar radiusi
    lambda_reg = None    # Regularizatsiya parametri
    changed_data = None  # Nominal alomatlari miqdoriyga va barcha alomatlari [-1, -1] oraliqqa tushirilgan data
    last_row = None       # Harakteristik vektor
    e = None             # Anomallarning lokal soxasidagi gepershar radiusi
    all_indexes = None   # Anomal va anomal bo'lmagan obyektlarni ko'rsatuvchi vektor [faqat 0 va 1]
   
    def __init__(self, data):
        self.real_data = data[0:-1,:]
        self.last_row = data[-1,:].astype(int)
        self.changed_data = self.nominalToQuantitative()
        self.changed_data = self.minMaxScale()

    def nominalToQuantitative(self):
        row, _ = np.shape(self.real_data)
        new_data = self.real_data.copy().astype(float)
        for j in range(len(self.last_row)):
            if self.last_row[j] == 0:
                for i in range(row):
                    new_data[i][j] = np.count_nonzero(self.real_data[:,j] == self.real_data[i][j]) / row
        return new_data
    
    def minMaxScale(self):  # Normallashtirish [-1, 1]
        row, col = np.shape(self.changed_data)
        new_data = np.zeros((row, col))
        maxValue = np.max(self.changed_data, axis=0)
        minValue = np.min(self.changed_data, axis=0)
        for i in range(row):
            for j in range(col):
                    new_data[i][j] = 2 * (self.changed_data[i][j] - minValue[j]) / (maxValue[j] - minValue[j]) - 1
        return new_data

    def euiclidenDistances(self, data, C): # Markaz va boshqa obyektlar o'rtasidagi masofalar
        return np.linalg.norm(data - C, axis=1)

    def computeCenter(self, data, C, r):
        inner_objects = self.euiclidenDistances(data, C) <= r
        data_in = data[inner_objects]
        if len(data_in) == 0:
            return C
        return np.mean(data_in, axis=0)
    def computeRadius(self, data, C):
        return np.mean(self.euiclidenDistances(data, C))
    
    def lossFunction(self, data, C, r, lambda_reg):
        distances = self.euiclidenDistances(data, C)
        loss = np.sum(r**2 - distances**2)
        loss = np.clip(loss, -100, 100)
        return lambda_reg * (r**2) + 2 * 1.0 / (1 + np.exp(loss))

    def findHyperspere(self, tol = 1e-6, itar = 100, lambda_reg = 1):
        delta_data = self.changed_data
        delta_C = np.mean(delta_data, axis=0)
        delta_r = np.mean(self.euiclidenDistances(delta_data, delta_C))
        prev_obj_value = float('inf')
        for i in range(itar):
            delta_C = self.computeCenter(delta_data, delta_C, delta_r)
            delta_r = self.computeRadius(delta_data, delta_C)
            obj_value = self.lossFunction(delta_data, delta_C, delta_r, lambda_reg)
            # np.abs(prev_obj_value - obj_value) < tol:
            if prev_obj_value - obj_value <= tol:
                print(f'Itaratsiyalar soni: {i + 1}')
                break
            prev_obj_value = obj_value
        self.C = delta_C
        self.r = delta_r
    
    def findAnomalouses(self):        
        obj_anomal = self.euiclidenDistances(self.changed_data, self.C) < self.r
        all_indexes = obj_anomal.astype(int) # 0 - anomal, 1 - normal
        count_anomalouses = len(all_indexes) - sum(all_indexes)
        print('Count anomalouses: ',count_anomalouses)
        print('All indexes: ', all_indexes)
        # print('Real anomal objects:')
        # for i in range(len(all_indexes)):
        #     if all_indexes[i] == 0:
        #         print(self.real_data[i])
        self.all_indexes = all_indexes
    
    def eDensity(self, k = 3, interval = 1): # taqsimoq zichligi uchun radius(e) ni hisoblash. Har interval(10 chi) uzunligi bo'yicha obyektlarni olib tekshiradi. Tanlab olingan 50000 ta obyektlar uchun chiqqan naticha ichidan tanlab olingan 500 ta obyektdan olingan natija bilan taxminan bir xil.
        new_data = self.changed_data[::interval]
        row, _ = np.shape(new_data)
        knn_arr = np.zeros(row)
        for i in range(len(new_data)):
            distances = np.linalg.norm((new_data[i] - self.changed_data), axis=1)
            distances.sort()
            knn_arr[i] = distances[k]
        e = np.mean(knn_arr)
        self.e = e

    def anomalNormalPercent(self):
        if self.e is None:
            self.eDensity(3, 1)
        if self.all_indexes is None:
            self.findAnomalouses(3, 1)
        all_indexes = self.all_indexes
        anomals_count = len(all_indexes) - np.sum(all_indexes)
        distDen = np.zeros((anomals_count, 5)) # [12, 30, 70, 23, 0.41] --> 12 indexli anomal, atrofida 30% anomal, 70% normal, 23 ta anomal, 0.41 - taqsimot zichligi
        j = 0
        for i in range(len(all_indexes)):
            if all_indexes[i] == 0:
                distances = np.linalg.norm(self.changed_data[i] - self.changed_data, axis=1)
                e_inner_objs = (distances < self.e).astype(int)
                inner_distances = distances[e_inner_objs == 1] # o'zigacha bo'lgan masofa(0) ni ham olib keladi
                e_inner_objs[i] = 0 # o'zini chiqarib ketish
                inner_objs_count = np.sum(e_inner_objs)
                if (inner_objs_count == 0):
                    distDen[j, 0] = i
                    distDen[j, 1] = 0
                    distDen[j, 2] = 0
                    distDen[j, 3] = 0
                    distDen[j, 4] = 0
                else:
                    inner_normal_count = np.sum(all_indexes * e_inner_objs)
                    inner_anomal_count = inner_objs_count - inner_normal_count
                    anomals_percent = inner_anomal_count * 100 / inner_objs_count
                    normal_percent = 100 - anomals_percent
                    distDen[j, 0] = i
                    distDen[j, 1] = round(anomals_percent, 2)
                    distDen[j, 2] = round(normal_percent, 2)
                    distDen[j, 3] = inner_anomal_count
                    distDen[j, 4] = self.distributionDensity(inner_distances, self.e)
                j+=1
        print(distDen)
    
    def distributionDensity(self, distances, e): # taqsimot zichligi, formula bo'yicha
        p = 0
        for dist in distances:
            if dist != 0:      # o'ziga bo'lgan masofa(0) ni chiqarib ketish
                p += 1 - dist/e
        return p
    
    def centerKNeighbors(self, k = 3): # markazga k ta yaqin obyektlarni topish
        distances = np.linalg.norm((self.changed_data - self.C), axis=1)
        by_index_sort = np.argsort(distances)
        result_indexes = by_index_sort[:k]
        return result_indexes

    def eachOtherDistances(self): # gipershar markaziga eng yaqin obyekt topiladi va qolgan yaqinlarigacha bo'lgan masofalar topiladi
        result_indexes = self.centerKNeighbors()
        currentObjs = self.changed_data[result_indexes]
        mostCloserObj = currentObjs[0]
        otherCloserObjs = currentObjs[1:]
        distances = np.linalg.norm(otherCloserObjs - mostCloserObj, axis=1)
        print('Markaz: ',self.C)
        print('Eng yaqini: ',mostCloserObj)
        print('Markazdan eng yaqin obyektgacha bo\'lgan masofa:', np.linalg.norm(self.C - mostCloserObj))
        print('Bir-birlari orasidagi masofalar:', distances)

    def setLabel(self):
        self.last_row = np.append(self.last_row, 0)
        self.last_row = self.last_row.reshape(1, -1)
        target_col = self.all_indexes.reshape((self.real_data.shape[0], 1))
        re_S = np.hstack((self.real_data, target_col))
        re_S = np.vstack((re_S, self.last_row))
        last_row_str = ['%g'] * len(self.last_row[0])
        np.savetxt('re-meteo.dat', re_S, fmt=last_row_str)