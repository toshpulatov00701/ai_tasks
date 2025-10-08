import numpy as np

# def sortArray(arr): # Shu ko'rinishda tartiblash zarur. Negaki bir xil kelib qolgan alomatlarning sinflari tartibi hom alomat tartibida kelishi kerak.
#     for i in range(len(arr)):
#         for j in range(i+1, len(arr)):
#             if arr[i,0] > arr[j, 0]:
#                 delta = np.copy(arr[i]) 
#                 arr[i] = arr[j]
#                 arr[j] = delta
#     return arr

# data = np.loadtxt('datasets/testdata.txt')
# sorted_col = sortArray(data[:,[0, -1]])
# print(sorted_col)
# print('----')
# print(sorted_col[3:,-1])

# d1 = np.sum(sorted_col[3:,-1] == 2.)
# print(d1)
# for i in range(len(sorted_col)):
#     for j in range(i+1, len(sorted_col)+1):
#         print(sorted_col[i:j])
#         print('--------')
    # print(f'{sorted_col[:i,:]}')
    # print('--')
    # print(f'{sorted_col[i:,:]}')
    # print('----------------------------')
    # # d1 = len(np.where(sorted_col[i:,:] == 1.)[1])
    # d1 = np.sum(sorted_col[i:,:] == 1)
    # print(d1)
    # break

data = np.random.randint(10, 99, size=(300, 10))
classes = np.random.randint(1, 3, size=(300,1))
res_data = np.hstack((data, classes))
print(res_data[:3,:])
np.savetxt('datasets/testdata.txt', res_data, fmt='%d')

# def rekursiya(arr):
#     if len(arr) == 1: return arr[0]
#     return str(arr[0]) + ' - ' + str(rekursiya(arr[1:]))

# d = np.array([2, 6, 4, 8, 10, 20])
# print(d[:6])