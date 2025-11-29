import numpy as np
from dbscan_3_type import DBSCAN3Type
from myDBSCAN import ClassicDBSCAN
from knp_length import KNP
from distance_two_matrixes import DTMatrixes
from distance_metrics import DistMetrics

class ClusteringByLoop:
    # res_labels - mx2 ko'rinishdagi natijaviy klaster nomlari. 0 ustun klaster nomi, 1 ustun bosqich nomeri

    def __init__(self, data, k, anom_percent, metric_type, normal_type=None, number_parts=500):
        
        self.data = data                            # Harakteristik vektorga ega bo'lgan dastlabki data
        m, _ = data.shape
        self.m = m - 1
        self.k = k                                  # Qo'shnilar soni
        self.anom_percent = anom_percent
        self.metric_type = metric_type
        self.normal_type = normal_type
        self.number_parts = number_parts            # Ekstrimum(minimum)ni topish uchun bo'laklar soni
        self.firstStep()
    
    def firstStep(self):
        k = self.k
        m = self.m
        data = self.data
        objDb = DBSCAN3Type(data, k=k, metric_type=self.metric_type, normal_type=self.normal_type)
        eks_lambda = objDb.find_extrimums(self.anom_percent, self.number_parts)
        r = objDb.e_avarage * eks_lambda
        print('Foydalanilayotgan r:', r)
        db = ClassicDBSCAN(data, eps=r, min_samples=k, metric_type=self.metric_type, normal_type=self.normal_type)
        clasters_name = np.unique_all(db.c_labels).values
        db_status = db.get_statuses3()
        
        # Natijalarni ko'rish
        print('Klaster nomlari:', clasters_name)
        print('Obyektlar miqdorlari(birinchisi anomal):', np.unique_all(db.c_labels).counts)
        print(f'Anomallar soni: {np.sum(db_status == 3)}',)
        print(f'Anomallar(%): {np.sum(db_status == 3) * 100 / len(data[:-1,:])}')
        
        arr_ones = np.ones((m, 1), dtype=int)
        self.res_labels = np.hstack((db.c_labels.reshape(-1,1), arr_ones))

    def objs_in_cores(self, anomal_objs, min_radiuses):
        dm = DistMetrics(anomal_objs, metric_type=self.metric_type, normal_type=self.normal_type)
        distances_matrix = dm.distance_matrix
        m = dm.m
        groups = np.zeros((m, 2), dtype=object)
        k = self.k
        if self.metric_type == 'euclidean':
            for i in range(m):
                groups[i, 0] = np.where(distances_matrix[i] <= min_radiuses[i])[0]   # Yadro nuqta (Core point) – agar ε-radius ichida kamida minPts (shu obyektning o‘zi ham qo‘shib hisoblamoqda) qo‘shnisi bo‘lsa. Masofalar kvadratlari olingani uchun e**2. [min_radiuses ham kvadrati bo'lib kelgani uchun undan **2 olib tashlangan]
                if len(groups[i, 0]) >= k:                                           # groups birinchi ustunida ichiga tushuvchi obyektlar, ikkinchi ustunida esa 1-yardoriy, 0-yadroviy emas
                        groups[i, 1] = 1
                else:
                        groups[i, 1] = 0
        else:
            for i in range(m):
                groups[i, 0] = np.where(distances_matrix[i] <= min_radiuses[i])[0]
                if len(groups[i, 0]) >= k:
                        groups[i, 1] = 1
                else:
                        groups[i, 1] = 0
        return groups        

    def otherSteps(self):
        data = self.data
        m = self.m
        k = self.k
        ids = np.ones((m + 1))                                    # Bosqichlar oralig'ida obyekt indexsini saqlash uchun
        for i in range(m): ids[i]=i
        data = np.hstack((ids.reshape(-1, 1), data))
        labels = self.res_labels
        anomal_m = np.inf
        while anomal_m > k:
            anomals_index = np.where(labels[:, 0] == -1)[0]
            clastered_index = np.where(labels[:, 0] != -1)[0]     # Barcha klasterlarni olish
            anomal_objs = np.vstack((data[anomals_index], data[-1,:]))
            claster_objs = np.vstack((data[clastered_index], data[-1,:])) 
            obj_dtm = DTMatrixes(anomal_objs[:,1:], claster_objs[:,1:], self.metric_type, self.normal_type)
            dist_anom_claster = obj_dtm.distance_matrix          # Anomallardan klasterlargacha bo'lgan masofalar(evlid bo'lsa kvadrati keladi)
            min_radiuses = np.min(dist_anom_claster, axis=1)
            anomal_m = len(anomals_index)
            objs_in_cores = self.objs_in_cores(anomal_objs[:, 1:], min_radiuses)
            result = np.hstack((np.ones((anomal_m, 1), dtype=int) * (-2), objs_in_cores[:, 1].reshape(-1, 1)))              # Klasterlar va anomallarni belgilash uchun
            t = 0                                                # Sinf nomi
            for i in range(anomal_m):
                
                if (result[i, 0] == -2) & (result[i, 1] == 0):
                    result[i, 0] = -1
                else:
                    res_in = result[objs_in_cores[i, 0]]
                    if np.any((res_in[:, 0] >= 0) & (res_in[:, 1] == 1)):  
                        core_claster = res_in[(res_in[:, 0] >= 0) & (res_in[:, 1] == 1)]  # Biron klasterga tegishli va yadroviy bo'lganlari 
                        u_c_claster = np.unique(core_claster[:, 0])
                        setter_claster = u_c_claster[0]
                        for u_c in u_c_claster:
                            result[result[:, 0] == u_c, 0] = setter_claster
                        obj_in = objs_in_cores[i, 0]
                        for o_in in obj_in:
                            if result[o_in, 0] < 0:
                                result[o_in, 0] = setter_claster
                    else:                                                  # Ichida ham yadroviy, ham biron klasterga tegishlilari yo'q
                        if result[i, 1] == 1:
                            obj_in = objs_in_cores[i, 0]
                            for o_in in obj_in:
                                if result[o_in, 0] < 0:
                                    result[o_in, 0] = t
                            t += 1
            
            result = result[:, 0]
            r_u = np.unique(result[np.where(result != -1)[0]])
            if len(r_u) > 0:
                counter_step = np.max(labels[:, 1]) + 1
                for i in range(len(r_u)):
                    claster_ids = anomal_objs[np.where(result == r_u[i])[0]][:,0].astype(int)
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

    def colculate_KNP_Quality(self):
        data = self.data
        data_obj = DistMetrics(data=data, metric_type=self.metric_type, normal_type=self.normal_type)
        data = np.vstack((data_obj.normal_data, data[-1,:]))
        labels = self.otherSteps()
        u_claster = np.unique(labels[:, 0])
        u_step = np.unique(labels[:, 1])
        arr_knp = []
        quality_all = 0
        for u_s in u_step:
            sum_knp = 0
            c_count_step = 0                       # u_s bosqichdagi klasterlar soni
            checker = False
            u_claster = u_claster[u_claster != -1]
            quality = 0
            
            for u_c in u_claster:
                delta_data = np.where((labels[:, 0] == u_c) & (labels[:, 1] == u_s))[0]
                
                delta_data = data[delta_data]
                if len(delta_data) > 0:
                    G_ip = len(delta_data)
                    quality += G_ip**2
                    checker = True
                    delta_data = np.vstack((delta_data, data[-1,:]))
                    
                    obj_KNP = KNP(delta_data, self.metric_type, normal_type=None)
                    
                    c_count_step += 1
                    sum_knp += obj_KNP.get_sum_distances()
            #         break # ol
            # break # ol                    
            obj_step_count = np.sum((labels[:, 0] != -1) & (labels[:, 1] == u_s)) # Har bir bosqichdagi obyektlar soni
            omega_Zi = quality / (obj_step_count**2)
            quality_all += obj_step_count * omega_Zi
            if checker:
                arr_knp.append(sum_knp / (obj_step_count - c_count_step))
            
            ## Sifatini hisoblash
            print()
            print(f'{u_s} - bosqich sifati: {omega_Zi}')
        print()
        print('Umumiy sifat:', quality_all/self.m)
        return np.array(arr_knp)

# data = np.loadtxt('datasets/wine_1_new.txt', dtype=float)
# metric_type='euclidean'
# normal_type='normalization'
# k = 3
# anom_percent = 60

# print('Dataset: wine_1')
# print('Metrika: ', metric_type)
# print('Normalizatsiya: [-1, 1]')
# print('k=', k)
# print('anomlar(%): ', anom_percent)

# objClaster = ClusteringByLoop(data, k, anom_percent, metric_type, normal_type, 100)
# knp_by_steps = objClaster.colculate_KNP_Quality()

# # Natijalarni chiqarish
# labels = objClaster.res_labels
# for step in np.unique(labels[:,1]):
#     print()
#     print(f'{step} - BOSQICH:')
#     u_clasters = np.unique(labels[:,0])
#     u_clasters = u_clasters[u_clasters != -1]
#     for claster in u_clasters:
#         soni = np.sum((labels[:, 0] == claster) & (labels[:, 1] == step))
#         if soni > 0:
#             print(f'{claster} - klaster:')
#             print('Obyektlar:', np.where((labels[:, 0] == claster) & (labels[:, 1] == step))[0])
#             print('Obyektlar soni:', soni)
#     print('KNP uzunligi:', knp_by_steps[step - 1])
#     print('Zichligi:', 1 / knp_by_steps[step - 1])

# anomals = np.where(labels[:, 0] == -1)[0]
# print()
# print('Anomallar: ', anomals)
# print('Anomallar soni: ', len(anomals))