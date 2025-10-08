# tanlanmani ko'rinishi: o'qituvchisiz(unlabled), harakteristik vektorga ega.
import numpy as np

def euiclidenDistances(S, C):
    return np.linalg.norm(S - C, axis=1)

def chebyshevDistances(S, C):
    return np.max(np.abs(S - C), axis=1)

def computeCenter(S, C, r, distance_type):
    if distance_type == 0:
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    inner_objects = compute_distances(S, C) <= r
    S_in = S[inner_objects]
    if len(S_in) == 0:
        return C
    return np.mean(S_in, axis=0)

def computeRadius(S, C, distance_type):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    return np.mean(compute_distances(S, C))

# 1 - loss funcsion Q(M) = (1-M)^2
def objectiveFunction_1(S, C, r, distance_type, lambda_reg = 1):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    distances = compute_distances(S, C)
    loss = np.sum(r**2 - distances**2)
    return lambda_reg * (r**2) + (1-loss)**2

# 2 - loss funcsion V(M) = (1-M)
def objectiveFunction_2(S, C, r, distance_type, lambda_reg = 1):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    distances = compute_distances(S, C)
    loss = np.sum(r**2 - distances**2)
    return lambda_reg * (r**2) + (1-loss)

# 3 - loss funcsion L(M) = 2*(1+e^M)^-1
def objectiveFunction_3(S, C, r, distance_type, lambda_reg = 1):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    distances = compute_distances(S, C)
    loss = np.sum(r**2 - distances**2)
    loss = np.clip(loss, -100, 100)
    return lambda_reg * (r**2) + 2 * 1.0 / (1 + np.exp(loss))

# 4 - loss funcsion L(M) = log2(1+e^-M)
def objectiveFunction_4(S, C, r, distance_type, lambda_reg = 1):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    distances = compute_distances(S, C)
    loss = np.sum(r**2 - distances**2)
    loss = np.clip(loss, -100, 100)
    return lambda_reg * (r**2) + np.log(1 + np.exp(-loss)/np.log(2))

# 5 - loss funcsion L(M) = e^-M
def objectiveFunction_5(S, C, r, distance_type, lambda_reg = 1):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    distances = compute_distances(S, C)
    loss = np.sum(r**2 - distances**2)
    loss = np.clip(loss, -100, 100)
    return lambda_reg * (r**2) + np.exp(-loss)

# 6 - loss funcsion L(M) = max(0, -M)
def objectiveFunction_6(S, C, r, distance_type, lambda_reg = 1):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    distances = compute_distances(S, C)
    loss = np.sum(r**2 - distances**2)  
    return lambda_reg * (r**2) + np.max([0, -loss])

# Main function
def findHyperspere(S, distance_type, fun_index,  C_init = None, r_init = None, tol = 1e-6, itar = 100, lambda_reg = 1):
    objective_functions = [objectiveFunction_1, objectiveFunction_2, objectiveFunction_3, objectiveFunction_4, objectiveFunction_5, objectiveFunction_6]
    objective_function = objective_functions[fun_index]
    if C_init is None:
        C = np.mean(S, axis=0)
    else:
        C = C_init
    if r_init is None:
        if distance_type == 0: 
            compute_distances = euiclidenDistances
        elif distance_type == 1:
            compute_distances = chebyshevDistances
        r = np.mean(compute_distances(S, C))
    else:
        r = r_init

    prev_obj_value = float('inf')
    for i in range(itar):
        C = computeCenter(S, C, r, distance_type)
        r = computeRadius(S, C, distance_type)

        obj_value = objective_function(S, C, r, distance_type, lambda_reg)
        #np.abs(prev_obj_value - obj_value) < tol:
        if prev_obj_value - obj_value <= tol:
            # print(f'Itaratsiyalar soni: {i + 1}')
            break
        prev_obj_value = obj_value
    return C, r, prev_obj_value

def findAnomalouses(S, C, r, lastRow, distance_type):
    if distance_type == 0: 
        compute_distances = euiclidenDistances
    elif distance_type == 1:
        compute_distances = chebyshevDistances
    obj_anomal = compute_distances(S, C) < r
    all_indexes = obj_anomal.astype(int) # 0 - anomal, 1 - normal
    count_anomalouses = len(all_indexes) - sum(all_indexes)
    print('Count anomalouses: ',count_anomalouses)
    return all_indexes

def minMaxScale(S, lastRow):  # Normallashtirish [-1, 1]
    row, col = np.shape(S)
    new_S = np.zeros((row, col))
    S = normalision(S, lastRow)
    maxValue = np.max(S, axis=0)
    minValue = np.min(S, axis=0)
    for i in range(row):
        for j in range(col):
                new_S[i][j] = 2 * (S[i][j] - minValue[j]) / (maxValue[j] - minValue[j]) - 1
    return new_S

def normalision(S, lastRow): # nominal alomatlarni son ko'rinishiga o'tkazish
    row, _ = np.shape(S)
    new_S = S.copy().astype(float)
    for j in range(len(lastRow)):
        if lastRow[j] == 0:
            for i in range(row):
                new_S[i][j] = np.count_nonzero(S[:,j] == S[i][j]) / row
    return new_S

def eDensity(S, k, interval = 1): # taqsimoq zichligi uchun radius(e) ni hisoblash. Har interval(10 chi) uzunligi bo'yicha obyektlarni olib tekshiradi. Tanlab olingan 50000 ta obyektlar uchun chiqqan naticha ichidan tanlab olingan 500 ta obyektdan olingan natija bilan taxminan bir xil.
    new_S = S[::interval]
    row, _ = np.shape(new_S)
    knn_arr = np.zeros(row)
    for i in range(len(new_S)):
        distances = np.linalg.norm((new_S[i] - S), axis=1)
        distances.sort()
        knn_arr[i] = distances[k]
    e = np.mean(knn_arr)
    return e

def anomalNormalPercent(S, all_indexes, e):
    anomals_count = len(all_indexes) - np.sum(all_indexes)
    distDen = np.zeros((anomals_count, 5)) # [12, 30, 70, 23, 0.41] --> 12 indexli anomal, atrofida 30% anomal, 70% normal, 23 ta anomal, 0.41 - taqsimot zichligi
    j = 0
    for i in range(len(all_indexes)):
        if all_indexes[i] == 0:
            distances = np.linalg.norm(S[i] - S, axis=1)
            e_inner_objs = (distances < e).astype(int)
            # print(distances)
            # print(e_inner_objs)
            # print(distances[e_inner_objs == 1])
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
                distDen[j, 4] = distributionDensity(inner_distances, e)
            j+=1
    return distDen

def distributionDensity(distances, e): # taqsimot zichligi, formula bo'yicha
    p = 0
    for dist in distances:
        if dist != 0:      # o'ziga bo'lgan masofa(0) ni chiqarib ketish
            p += 1 - dist/e
    return p

def centerKNeighbors(S, C, k): # markazga k ta yaqin obyektlarni topish
    distances = np.linalg.norm((S - C), axis=1)
    by_index_sort = np.argsort(distances)
    result_indexes = by_index_sort[:k]
    r = np.linalg.norm(C - S[result_indexes[k-1]])
    return result_indexes, r

def eachOtherDistances(result_indexes, S, C): # gipershar markaziga eng yaqin obyekt topiladi va qolgan yaqinlarigacha bo'lgan masofalar topiladi
    currentObjs = S[result_indexes]
    mostCloserObj = currentObjs[0]
    otherCloserObjs = currentObjs[1:]
    distances = np.linalg.norm(otherCloserObjs - mostCloserObj, axis=1)
    print('Markaz: ',C)
    print('Eng yaqini: ',mostCloserObj)
    print('Markazdan eng yaqin obyektgacha bo\'lgan masofa:', np.linalg.norm(C - mostCloserObj))
    # print(otherCloserObjs)
    print('Bir-birlari orasidagi masofalar:', distances)
    return result_indexes

def setLabel(S, allindexes, last_row):
    last_row = np.append(last_row, 0)
    last_row = last_row.reshape(1, -1)
    target_col = allindexes.reshape((S.shape[0], 1))
    re_S = np.hstack((S, target_col))
    re_S = np.vstack((re_S, last_row))
    np.savetxt('re-meteo.dat', re_S, fmt='%g %g %g %g %g %g %g %g %d')


#*************************#

# S = np.loadtxt("meteo.dat")
S = np.array([
        [80, 100, 32, 12, 30],
        [76, 200, 28, 14, 30],
        [84, 200, 30, 10, 60],
        [ 5, 100, 99, 90, 60],
        [82, 100, 30,  8, 60],
        [ 1,   0,  1,  1,  0]
])
S = np.array([
    [1, 2, 1],
    [5, 4, 3],
    [3, 5, 1],
    [8, 4, 1],
    [6, 3, 3],
    [6, 4, 1],
    [7, 5, 1],
    [8, 8, 1],
    [4, 5, 3],
    [10, 10, 1],
    [10, 8, 1],
    [11, 10, 3],
    [11, 9, 3],
    [7, 7, 3],
    [1, 1, 0]
])
# dist_type = 0
# obj_fun_index = 0 
lastRow = S[-1,:].astype(int) # Characteristics vector
S = S[0:-1,:]
Main_S = S.copy().astype(float) # Anomallarni ko'rsatish uchun kerak
S = minMaxScale(S, lastRow)

C, r, prev_obj_value = findHyperspere(S, 0, 0)

print('old::')
print('C:', C)
print('r:', r)

# resss = np.zeros((10,1))
# # for i in range(2, 10):
# neighbors_C_indexes, neighbors_r = centerKNeighbors(S, C, 3)
# resss[3][0] = neighbors_r
# print('k=', 3)
# print('r: ', neighbors_r)
# print('Yaqin obyektlar: ', neighbors_C_indexes)
# eachOtherDistances(neighbors_C_indexes, S, C)
# print('********************************')



all_indexes = findAnomalouses(S, C, r, lastRow, 0)

# setLabel(Main_S, all_indexes, lastRow)

# print('Center : ', C)
# print('R : ', r)
# print('Anomalouses:')
# for i in range(len(all_indexes)):
#     if all_indexes[i] == 0:
#         print(Main_S[i])

e = eDensity(S, 3, 1)
print('e : ', e)
distribution_persents = anomalNormalPercent(S, all_indexes, e)
print(distribution_persents)
# t = 0
# for i in range(len(distribution_persents)):
#     if distribution_persents[i][2] != 0.0:
#         print(distribution_persents[i])
#         t+=1
# print(f't={t}')



# np.set_printoptions(suppress=True, precision=3)
# print('Anomallarni taqsimot zichliklari: \n', distribution_persents)

# distance type 0 - euicliden, 1 - chebyshev 
# for i in range(2):
#     print(f"\n*******{i} -- metric*****\n")
#     for j in range(6):
#         print(f"\n----------{j+1} -- loss function -------------\n")
#         C, r, prev_obj_value = findHyperspere(S, i, j)
#         anomalouses = findAnomalouses(S, C, r, i)
#         print('C:', C)
#         print('r:', r)
#         print('Min:', prev_obj_value)
#         # print('Anomallar:\n', anomalouses)
#         print('Anomallar soni: ', len(anomalouses))