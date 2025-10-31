# Uzatiladigan dataning harakteristik vektori bo'lishi shart.

import numpy as np
import sys
from distanceMetrics import dMetrics

class ClassicDBSCAN(dMetrics):
    min_samples = None                   
    eps = None
    distances_matrix = None    # Obyektlar o'rtasidagi masofalar.
    c_labels = None            # Klasterlar
    metric_type = None
        
    def __init__(self, data, eps, min_samples, metric_type, normal_type=None):
        super().__init__(data, metric_type, normal_type)
        sys.setrecursionlimit(int((self.m + 1) * self.m / 2))                  # Klasterlarni yig'ayotganda rekursiv funksiyaning ichiki kirishi python ruxsat etgan(1000) dan oshganda ham ishlashi uchun. Eng chuqur kirish barcha obyektlar bitta klasterga tushganda bo'ladi. Bizdagi 300ta obyekt holatida 1-obyektga kirish 999, 2-obyektga kirish 998, 3-obyektga kirish 997,... Oxirgi obyektlarga k ning qiymatidan kelib chiqib to'xtaydi.
        self.eps= eps
        self.min_samples = min_samples
        self.metric_type = metric_type
        self.separateClastering()

    def objsInCores(self):
        distances_matrix = self.distance_matrix
        m = self.m
        eps= self.eps
        groups = np.zeros(m, dtype=object)
        if self.metric_type == 'euclidean':
            for i in range(m):
                    groups[i] = np.where(distances_matrix[i] <= eps**2)[0]   # Yadro nuqta (Core point) – agar ε-radius ichida kamida minPts (shu obyektning o‘zi ham qo‘shib hisoblamoqda) qo‘shnisi bo‘lsa. Masofalar kvadratlari olingani uchun e**2.
        else:
            for i in range(m):
                    groups[i] = np.where(distances_matrix[i] <= eps)[0]
        return groups

    def separateClastering(self):
        min_samples = self.min_samples
        m = self.m
        objs_in_cores = self.objsInCores()                # Har bir sinf va epsradiusdagi obyektlar
        result = np.ones(m, dtype=int) * (-2)             # Klasterlar va anomallarni belgilash uchun
        t = 0                                             # Sinf nomi
        for i in range(m):
            if result[i] == -2 or result[i] == -1:
                if len(objs_in_cores[i]) < min_samples:
                    result[i] = -1
                else:
                    result[i] = t
                    def setClaster(obj_in_core, t):                    
                        for c in obj_in_core:
                            result[c] = t
                            if len(objs_in_cores[c]) >= min_samples:
                                new_arr = np.delete(objs_in_cores[c], np.where(objs_in_cores[c] == c))      # O'zini olib tashla.
                                new_arr = np.delete(new_arr, np.where((result[new_arr] != -2) == True))     # Biron klasterga tegishli bo'lganlarini chiqarib tashla. Unda anomal bo'lmaydi. Chunki biron yadro r atrofidagi obyekt anomal hisoblanmay. U yoki yadro yoki chegaraviy bo'ladi.
                                setClaster(new_arr, t)
                    new_arr = np.delete(objs_in_cores[i], np.where(objs_in_cores[i] == i))
                    new_arr = np.delete(new_arr, np.where((result[new_arr] > -1) == True))                  # -1 va -2 bo'lganlarnigini qayta ko'rib chiq. Biron klasterga ega bo'lganlarni olib tashlash
                    setClaster(new_arr, t)
                    t += 1
        self.c_labels = result

    def getStatuses(self):
        m = self.m
        c_labels  = self.c_labels
        obj_statuses = np.ones(m, dtype=int)
        objs_in_cores = self.objsInCores()
        for i in range(m):
            if len(objs_in_cores[i]) >= self.min_samples:
                obj_statuses[i] = 1                                                  # Yadroviy
            elif c_labels[i] != -1 and len(objs_in_cores[i]) < self.min_samples:
                obj_statuses[i] = 2                                                  # Chegaraviy
            elif c_labels[i] == -1:
                obj_statuses[i] = 3                                                  # Anomal
        return obj_statuses