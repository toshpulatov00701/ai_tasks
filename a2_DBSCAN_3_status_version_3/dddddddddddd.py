import numpy as np
from dbscan3Type import DBSCAN3Type
from myDBSCAN import ClassicDBSCAN
from KNP_Length import KNP
from distanceTwoMatrixes import dtMatrixes
from distanceMetrics import dMetrics

class ClusteringByLoop:
    metric_type = None
    normal_type = None
    k = None                     # Qo'shnilar soni
    data = None                  # Harakteristik vektorga ega bo'lgan dastlabki data
    m = None                     
    number_parts = None          # Ekstrimum(minimum)ni topish uchun bo'laklar soni
    res_labels = None            # mx2 ko'rinishdagi natijaviy klaster nomlari. 0 ustun klaster nomi, 1 ustun bosqich nomeri

    def __init__(self, data, k, anom_percent, metric_type, normal_type=None, number_parts=500):
        self.data = data
        m, _ = data.shape
        self.m = m - 1
        self.k = k
        self.anom_percent = anom_percent
        self.metric_type = metric_type
        self.normal_type = normal_type
        self.number_parts = number_parts
        self.firstStep()
    
    def firstStep(self):
        k = self.k
        m = self.m
        data = self.data
        objDb = DBSCAN3Type(data, k=k, metric_type=self.metric_type, normal_type=self.normal_type)
        eks_lambda = objDb.findExtrimums(self.anom_percent, self.number_parts)
        r = objDb.e_avarage * eks_lambda
        db = ClassicDBSCAN(data, eps=r, min_samples=k, metric_type=self.metric_type, normal_type=self.normal_type)
        clasters_name = np.unique_all(db.c_labels).values
        db_status = db.getStatuses3()
        
        # Natijalarni ko'rish
        print('klaster nomlari:', clasters_name)
        print('klaster miqdorlari(birinchisi anomal):', np.unique_all(db.c_labels).counts)
        print(f'Anomallar soni: {np.sum(db_status == 3)}',)
        print(f'Anomallar(%): {np.sum(db_status == 3) * 100 / len(data[:-1,:])}')
        
        arr_ones = np.ones((m, 1), dtype=int)
        self.res_labels = np.hstack((db.c_labels.reshape(-1,1), arr_ones))

    def objsInCores(self, anomal_objs, min_radiuses):
        dm = dMetrics(anomal_objs, metric_type=self.metric_type, normal_type=self.normal_type)
        distances_matrix = dm.distance_matrix
        m = dm.m
        groups = np.zeros(m, dtype=object)
        if self.metric_type == 'euclidean':
            for i in range(m):
                groups[i] = np.where(distances_matrix[i] <= min_radiuses[i]**2)[0]   # Yadro nuqta (Core point) – agar ε-radius ichida kamida minPts (shu obyektning o‘zi ham qo‘shib hisoblamoqda) qo‘shnisi bo‘lsa. Masofalar kvadratlari olingani uchun e**2.
        else:
            for i in range(m):
                groups[i] = np.where(distances_matrix[i] <= min_radiuses[i])[0]
        return groups        

    def otherSteps(self):
        data = self.data
        m = self.m
        k = self.k
        ids = np.ones((m + 1))                         # Bosqichlar oralig'ida obyekt indexsini saqlash uchun
        for i in range(m): ids[i]=i
        data = np.hstack((ids.reshape(-1, 1), data))
        labels = self.res_labels
        anomal_m = np.inf
        while anomal_m > k:
            anomals_index = np.where(labels[:, 0] == -1)[0]
            clastered_index = np.where(labels[:, 0] != -1)[0]     # Barcha klasterlarni olish
            anomal_objs = np.vstack((data[anomals_index], data[-1,:]))
            claster_objs = np.vstack((data[clastered_index], data[-1,:])) 
            obj_dtm = dtMatrixes(anomal_objs[:,1:], claster_objs[:,1:], self.metric_type, self.normal_type)
            dist_anom_claster = obj_dtm.distance_matrix          # Anomallardan klasterlargacha bo'lgan masofalar
            min_radiuses = np.min(dist_anom_claster, axis=1)
            anomal_m = len(anomals_index)
            objs_in_cores = self.objsInCores(anomal_objs[:, 1:], min_radiuses)
            result = np.ones(anomal_m, dtype=int) * (-2)
            t = 0
            for i in range(anomal_m):
                if result[i] == -2 or result[i] == -1:
                    if len(objs_in_cores[i]) < k:
                        result[i] = -1
                    else:
                        result[i] = t
                        def setClaster(obj_in_core, t):                    
                            for c in obj_in_core:
                                result[c] = t
                                if len(objs_in_cores[c]) >= k:
                                    new_arr = np.delete(objs_in_cores[c], np.where(objs_in_cores[c] == c))      # O'zini olib tashla.
                                    new_arr = np.delete(new_arr, np.where((result[new_arr] != -2) == True))     # Biron klasterga tegishli bo'lganlarini chiqarib tashla. Unda anomal bo'lmaydi. Chunki biron yadro r atrofidagi obyekt anomal hisoblanmay. U yoki yadro yoki chegaraviy bo'ladi.
                                    setClaster(new_arr, t)
                        new_arr = np.delete(objs_in_cores[i], np.where(objs_in_cores[i] == i))
                        new_arr = np.delete(new_arr, np.where((result[new_arr] > -1) == True))                  # -1 va -2 bo'lganlarnigini qayta ko'rib chiq. Biron klasterga ega bo'lganlarni olib tashlash
                        setClaster(new_arr, t)
                        t += 1
            r_u = np.unique(result[np.where(result != -1)[0]])
            if len(r_u) > 0:
                counter_step = np.max(labels[:, 1]) + 1
                for i in range(0, len(r_u)):
                    claster_ids = anomal_objs[np.where(result == i)[0]][:,0].astype(int)
                    counter_claster = np.max(labels[:, 0]) + 1
                    labels[claster_ids, 0] = counter_claster
                    labels[claster_ids, 1] = counter_step
            anomal_m_end = len(np.where(labels[:, 0] == -1)[0])
            if anomal_m_end == anomal_m:
                break
            else:
                anomal_m = anomal_m_end
        self.res_labels = labels
        return  labels   

    def colculate_KNP(self):
        data = self.data
        labels = self.otherSteps()
        u_claster = np.unique(labels[:, 0])
        u_step = np.unique(labels[:, 1])
        arr_knp = []
        for u_s in u_step:
            sum_knp = 0
            c_count_step = 0          # u_s bosqichdagi klasterlar soni
            checker = False
            u_claster = u_claster[u_claster != -1]
            for u_c in u_claster:
                delta_data = np.where((labels[:, 0] == u_c) & (labels[:, 1] == u_s))[0]
                delta_data = data[delta_data]
                if len(delta_data) > 0:
                    checker = True
                    delta_data = np.vstack((delta_data, data[-1,:]))
                    np.savetxt(
                        f'datasets/claster-data/{u_s}-{u_c}-klaster.txt',
                        delta_data,
                        fmt='%g',
                        delimiter='\t'
                    )
                    obj_KNP = KNP(delta_data, self.metric_type, self.normal_type)
                    sum_knp += obj_KNP.getSumDistances()
                    # print('sum_knp:', obj_KNP.getSumDistances())
                    c_count_step += 1
            obj_step_count = np.sum((labels[:, 0] != -1) & (labels[:, 1] == u_s))
            if checker:
                arr_knp.append(sum_knp / (obj_step_count - c_count_step))
        return np.array(arr_knp)

data = np.loadtxt('datasets/testdata2.txt', dtype=float)
# data = data[:,:-1]
metric_type='euclidean'
normal_type='normalization'
k = 3
anom_percent = 60

print('Dataset: testdata2')
print('Metrika: ', metric_type)
print('Normalizatsiya: [-1, 1]')
print('k=', k)
print('anomlar(%): ', anom_percent)

objClaster = ClusteringByLoop(data, k, anom_percent, metric_type, normal_type, 100)
knp_by_steps = objClaster.colculate_KNP()

# Natijalarni chiqarish
labels = objClaster.res_labels
for step in np.unique(labels[:,1]):
    print()
    print(f'{step} - BOSQICH:')
    u_clasters = np.unique(labels[:,0])
    u_clasters = u_clasters[u_clasters != -1]
    for claster in u_clasters:
        soni = np.sum((labels[:, 0] == claster) & (labels[:, 1] == step))
        if soni > 0:
            print(f'{claster} - klaster:')
            print('Obyektlar:', np.where((labels[:, 0] == claster) & (labels[:, 1] == step))[0])
            print('Obyektlar soni:', soni)
    print('KNP uzunligi:', knp_by_steps[step - 1])
    print('Zichligi:', 1 / knp_by_steps[step - 1])

anomals = np.where(labels[:, 0] == -1)[0]
print()
print('Anomallar: ', anomals)
print('Anomallar soni: ', len(anomals))

