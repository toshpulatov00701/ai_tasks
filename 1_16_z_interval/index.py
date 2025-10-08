import numpy as np
import matplotlib.pyplot as plt

def gistogramma(i, j, z_1, z_2, R_ij):
        h = (z_2 - z_1) / 10 # diyapazon (10 ta bo'lakka bo'linganda, har bir bo'lak uzunligi)
        a = z_1
        gist_array = np.zeros(10, dtype=int)
        for t in range(10): # [a, b] # 10 ta bo'lakdagi chegaralar
            b = a + h
            if t == 9: b = z_2 # agar oxiriga borgan bo'lsa, oxirgisini chegara qilib ol. Chunki oxirgi elementni hisobdan chiqarib ketishi mumkin
            gist_items = np.where((R_ij >= a) & (R_ij <= b))[0]
            gist_array[t] = len(gist_items)
            a = b
        print(f'gist array: {gist_array} === sum->{np.sum(gist_array)}')
        gist_lables = np.arange(len(gist_array))
        plt.title(f'({i}, {j})')
        plt.bar(gist_lables, gist_array, color='skyblue')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

def findInterval(data):
    data_length = len(data)
    features_length = len(data[0])
    count_combinations = int(features_length * (features_length - 1)/2)
    Z_intervals = np.zeros((count_combinations, 4))
    row = 0
    for i in range(features_length):  # i, j - alomatlar kombinatsiyalari
        for j in range(i+1, features_length):
            P_i_items = data[:,i]
            P_i = np.mean(P_i_items)

            P_j_items = data[:,j]
            P_j = np.mean(P_j_items)

            R_ij = [data[k, i] / P_i - data[k, j] / P_j for k in range(data_length)] 
            z_1 = np.min(R_ij)
            z_2 = np.max(R_ij)

            print(f'({i}, {j}) => [{z_1}, {z_2}]')
            

            z_1_obj = np.where(R_ij == z_1)[0] # intervaldagi obyekt z1
            z_2_obj = np.where(R_ij == z_2)[0] # intervaldagi obyekt z2
            # gistogramma(i, j, z_1, z_2, R_ij)
            # print(f'Interval elements: ({z_1_obj}, {z_2_obj}) \n') # Intervaldagi elementlar
            Z_intervals[row, 0] = i
            Z_intervals[row, 1] = j         
            Z_intervals[row, 2] = z_1         
            Z_intervals[row, 3] = z_2
            row+=1         
    return Z_intervals
def defineNewObj(Ps, intervals, new_data):
     result = True # chegarada deb hisoblaymiz[chiqib ketsa false]
     row = 0
     print(f'Ps: {Ps}')
     print(f'intervals: {intervals}')
     print(f'new_data: {new_data}')
     features_length = len(new_data)
     for i in range(features_length):  # i, j - alomatlar kombinatsiyalari
        for j in range(i+1, features_length):
            z_ij_delta = new_data[i] / Ps[i] - new_data[j] / Ps[j]     
            print('z:', z_ij_delta)
            if z_ij_delta < intervals[row, 2] or z_ij_delta > intervals[row, 3]:
                 print(f'Xatolik indexlari:({i}, {j})')
                 result = False
            row+=1
     print(result)
     return result
#***************************************************#

data = np.loadtxt('dataset.txt', dtype=float)

intervals = findInterval(data)
Ps = np.mean(data, axis=0)
# new_data = np.array([7, 1, 5])
new_data = np.array([226, 120, 77, 31, 18, 20])



res = defineNewObj(Ps, intervals, new_data)
if not res:  # chiqib ketganlarni saqla
    with open('bilimlarbazasi.txt', 'a') as f:
        f.write('\n')  # yangi qator
        np.savetxt(f, new_data, fmt='%.4f', newline=' ')

print('natija: ', res)