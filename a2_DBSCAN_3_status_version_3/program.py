# Ushbu versiyada anomallar miqdori(%) kiritiladi. Shu asosida fiksirlangan k uchun r topadi. yadro, chegara - 1 va anomal - 2.
import numpy as np
from dbscan3Type import DBSCAN3Type
from myDBSCAN import ClassicDBSCAN

data = np.loadtxt('datasets/german.txt', dtype=float)
data = data[:,:-1]


metric_type='juravlov'
normal_type='normalization'
k = 15
anom_percent = 40

objDb = DBSCAN3Type(data, k=k, metric_type=metric_type, normal_type=normal_type)
eks = objDb.findExtrimums(anom_percent)

###############################
r = objDb.e_avarage * eks
db = ClassicDBSCAN(data, eps=r, min_samples=k, metric_type=metric_type, normal_type=normal_type)


print()
print('k=', k)
print(f'Anomallar: {anom_percent}%')
print('Natija:')
print('λmin, λmax: ', objDb.lambda_min_max, '(λmax Itaratsiya asosida topildi)')
print('λ ekstrimum(minimum): ', eks)
print('r=', r)

db_lables = db.c_labels
print('klasterlar: ',np.unique_all(db_lables).values)
print('har bir claster miqdori: ', np.unique_all(db_lables).counts)
all_claster_count = len(np.unique_all(db_lables).counts)
if np.unique_all(db_lables).values[0] == -1: all_claster_count -= 1
print('Umumiy klaster soni:', all_claster_count)

db_status = db.getStatuses3()
print('Anomallar : ', np.sum(db_status == 3) * 100 / len(data[:-1,:]))
print('Chegaraviylar : ', np.sum(db_status == 2) * 100 / len(data[:-1,:]))
print('Yadroviylar : ', np.sum(db_status == 1) * 100 / len(data[:-1,:]))