import numpy as np
from cbl import ClusteringByLoop

data = np.loadtxt('datasets/testdata2.txt', dtype=float)
metric_type = 'euclidean'
normal_type = None
k = 5              
anom_percent = 40

print('Dataset: testdata2')
print('Metrika: ', metric_type)
print('Normalizatsiya: None')
print('k=', k)
print('anomlar(%): ', anom_percent)

objClaster = ClusteringByLoop(data, k, anom_percent, metric_type, normal_type, 100)
knp_by_steps = objClaster.colculate_KNP_Quality()

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