# Uzatiladigan dataning harakteristik vektori bo'lishi shart.

import numpy as np
import sys
from distance_metrics import DistMetrics

class ClassicDBSCAN(DistMetrics):
    # c_labels - Klasterlar
        
    def __init__(self, data, eps, min_samples, metric_type, normal_type=None):
        super().__init__(data, metric_type, normal_type)
        sys.setrecursionlimit(int((self.m + 1) * self.m / 2))                  # Klasterlarni yig'ayotganda rekursiv funksiyaning ichiki kirishi python ruxsat etgan(1000) dan oshganda ham ishlashi uchun. Eng chuqur kirish barcha obyektlar bitta klasterga tushganda bo'ladi. Bizdagi 300ta obyekt holatida 1-obyektga kirish 999, 2-obyektga kirish 998, 3-obyektga kirish 997,... Oxirgi obyektlarga k ning qiymatidan kelib chiqib to'xtaydi.
        self.eps= eps                                                          # radius
        self.min_samples = min_samples                                         # k yaqin qo'shni
        self.separate_clastering()

    def objs_in_cores(self):                               # Har bir obyektning eps radiusiga kiruvchi obyektlar
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

    def separate_clastering(self):
        min_samples = self.min_samples
        m = self.m
        objs_in_cores = self.objs_in_cores()                # Har bir sinf va epsradiusdagi obyektlar
        result = np.ones(m, dtype=int) * (-2)             # Klasterlar va anomallarni belgilash uchun
        t = 0                                             # Sinf nomi
        for i in range(m):
            if result[i] == -2 or result[i] == -1:
                if len(objs_in_cores[i]) < min_samples:
                    result[i] = -1
                else:
                    result[i] = t
                    def set_claster(obj_in_core, t):                    
                        for c in obj_in_core:
                            result[c] = t
                            if len(objs_in_cores[c]) >= min_samples:
                                new_arr = np.delete(objs_in_cores[c], np.where(objs_in_cores[c] == c))      # O'zini olib tashla.
                                new_arr = np.delete(new_arr, np.where((result[new_arr] != -2) == True))     # Biron klasterga tegishli bo'lganlarini chiqarib tashla. Unda anomal bo'lmaydi. Chunki biron yadro r atrofidagi obyekt anomal hisoblanmay. U yoki yadro yoki chegaraviy bo'ladi.
                                set_claster(new_arr, t)
                    new_arr = np.delete(objs_in_cores[i], np.where(objs_in_cores[i] == i))
                    new_arr = np.delete(new_arr, np.where((result[new_arr] > -1) == True))                  # -1 va -2 bo'lganlarnigini qayta ko'rib chiq. Biron klasterga ega bo'lganlarni olib tashlash
                    set_claster(new_arr, t)
                    t += 1
        self.c_labels = result
        
    def get_statuses(self):               # Faqat anomal - 2, chegara va yadro - 1
        m = self.m
        c_labels  = self.c_labels
        obj_statuses = np.ones(m, dtype=int)
        objs_in_cores = self.objs_in_cores()
        for i in range(m):
            if len(objs_in_cores[i]) >= self.min_samples:
                obj_statuses[i] = 1                                                  # Yadroviy
            elif c_labels[i] != -1 and len(objs_in_cores[i]) < self.min_samples:
                obj_statuses[i] = 1                                                  # Chegaraviy
            elif c_labels[i] == -1:
                obj_statuses[i] = 2                                                  # Anomal
        return obj_statuses
    
    def get_statuses3(self):
        m = self.m
        c_labels  = self.c_labels
        obj_statuses = np.ones(m, dtype=int)
        objs_in_cores = self.objs_in_cores()
        for i in range(m):
            if len(objs_in_cores[i]) >= self.min_samples:
                obj_statuses[i] = 1                                                  # Yadroviy
            elif c_labels[i] != -1 and len(objs_in_cores[i]) < self.min_samples:
                obj_statuses[i] = 2                                                  # Chegaraviy
            elif c_labels[i] == -1:
                obj_statuses[i] = 3                                                  # Anomal
        return obj_statuses

# data = np.loadtxt('datasets/testdata2.txt', dtype=float)
# metric_type='euclidean'
# normal_type='normalization'
# k = 15
# r = 0.48164513185884156 * 0.7209064582519837
# db = ClassicDBSCAN(data, eps=r, min_samples=k, metric_type=metric_type, normal_type=normal_type)
# clasters_name = np.unique_all(db.c_labels).values
# db_status = db.get_statuses3()

# # Natijalarni ko'rish
# print('klaster nomlari:', clasters_name)
# print('klaster miqdorlari(birinchisi anomal):', np.unique_all(db.c_labels).counts)
# print(f'Anomallar soni: {np.sum(db_status == 3)}',)
# print(f'Anomallar(%): {np.sum(db_status == 3) * 100 / len(data[:-1,:])}')