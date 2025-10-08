# Xatoligi bor.
import numpy as np

class firstCriterian:
    l = None              # sinflar soni, intervallar soni
    K_arrays = None       # Sinflar va ularning mos soni
    data = None           # Dastlabki dataset
    def __init__(self, data):
        self.data = data
        self.set_l_K()

    def set_l_K(self):
        delta_data = self.data
        unique_items = np.unique_counts(delta_data[:,-1])
        self.l = len(unique_items[0])
        self.K_arrays = unique_items
    
    def buildDeter2D(self, sorted_classes):  # sorted_classes - tartiblangan alomat bo'yicha sinflarning joylashuvi 
        classes_name = self.K_arrays[0]
        classes_colunt = len(classes_name)
        D = np.zeros((classes_colunt, len(sorted_classes) + 1))
        _, cols = np.shape(D)
        for p in range(classes_colunt):
            for i in range(cols):
                if i == 0 :
                    D[p, i] = 0
                    continue
                if sorted_classes[i - 1] == classes_name[p]:
                    D[p, i] = D[p, i - 1] + 1
                else:
                    D[p, i] = D[p, i - 1]
        return D
    
    def getColSortedIndex(self, sorted_col):
        unique_indexes = np.unique_all(sorted_col)[1]
        unique_indexes = np.append(unique_indexes, len(sorted_col))
        return unique_indexes.tolist()
    
    def colculateCriteria(self, deter_2D, interval_array):
        left_numerator = self.leftNumerator(deter_2D, interval_array)
        left_denominator = self.leftDenominator()
        right_numerator = self.rightNumerator(deter_2D, interval_array)
        right_denominator = self.rightDenominator()
        result = (left_numerator / left_denominator) * (right_numerator / right_denominator)
        return float(result)
    
    def rightDenominator(self): # chap maxraj
        delta_K_arrays = self.K_arrays
        m = np.sum(delta_K_arrays[1])
        res_sum = 0
        for i in range(self.l):
            res_sum += delta_K_arrays[1][i] * (m - delta_K_arrays[1][i])
        return res_sum 

    def rightNumerator(self, deter_2D, interval_array): # o'ng surat
        delta_K_arrays = self.K_arrays
        m = np.sum(delta_K_arrays[1])
        l = self.l
        s_outer = 0
        for p in range(l):
            sum_u_j_p = np.sum(deter_2D[:, interval_array[p][1]] - deter_2D[:, interval_array[p][0]])
            s_inner = 0
            for i in range(l):
                u_i_p = deter_2D[i, interval_array[p][1]] - deter_2D[i, interval_array[p][0]]
                s_inner += u_i_p * (m - delta_K_arrays[1][i] - sum_u_j_p + u_i_p)
            s_outer += s_inner
        return s_outer
        
    def leftDenominator(self): # chap maxraj
        delta_K_arrays = self.K_arrays
        res_sum = 0
        for i in range(self.l):
            res_sum += delta_K_arrays[1][i] * (delta_K_arrays[1][i] - 1)
        return res_sum 

    def leftNumerator(self, deter_2D, interval_array): # chap surat
        l = self.l
        s_outer = 0
        for p in range(l):
            s_inner = 0
            for i in range(l):
                u_i_p = deter_2D[i, interval_array[p][1]] - deter_2D[i, interval_array[p][0]]
                s_inner += (u_i_p - 1) * u_i_p
            s_outer += s_inner
        return s_outer

    def checkNumberInIndexes(self, n, p, indexes): # n son(127), p xonalar soni(3), indexes kelyotgan sonni raqamlari shu massivda uchrashini tekshirish
        arr = []                    # kelgan n sonni raqamlari bo'yicha massivga o'tkazish
        for i in range(1, p+1):
            t = n%10
            arr.append(t)
            if not(t in indexes):
                return False, arr
            n //= 10
        arr.reverse()
        if not(arr == sorted(arr)):
            return False, arr
        if not(len(np.unique(arr)) == p):  # o'sish tartibida bo'lishi shart
            return False, arr
        return True, arr

    def getMaxCriterianAndInterval(self, arr):
        max_item = -1
        j = -1
        for i in range(len(arr)):
            if max_item < arr[i][0]:
                j = i
                max_item = arr[i][0]
        return j
    
    def sortResult(self, res_array, sorted_col):
        # [print(res_array[i]) for i in range(len(res_array))]
        # print(sorted_col)
        scores = [item[0] for item in res_array]
        sorted_criterian_value = np.argsort(scores)[::-1]

        # print(f'{sorted_col[0]}___{res_array[0][1][0][1]}___{res_array[0][1][2][1]}')
        

    def mainFun(self):
        delta_data = self.data
        l = self.l
        _, cols = np.shape(delta_data)
        criterian_all_cols = []
        for c in range(0, cols-1):
            sorted_data = data[data[:, c].argsort()]
            # [print(sorted_data[i,0], ' ', sorted_data[i,-1]) for i in range(len(sorted_data))]
            sorted_indexes = self.getColSortedIndex(sorted_data[:,c])    # tartiblangan va unikal bo'lgan qiymatlar
            # print(sorted_indexes)
            
            deter_2D = self.buildDeter2D(sorted_data[:, -1])
            # [print(deter_2D[0, i]) for i in range(len(deter_2D[0]))]
            indexes = list(range(1, len(sorted_indexes) + 1))  # shu raqamlardan hosil qilinishi mumkin sonlarga nisbatan tekshirish uchun
            # print(indexes)
            
            f_num = 10**(l - 1)                                # agar p = 3 bo'lsa 100-199 oraliqdagi sonlarni hosil qilib olamiz. Shu usul orqali mumkin bo'lgan intervallarni ko'rib chiqamiz
            criterian_by_col = []                              # bitta ustundagi mumkin bo'lgan intervallarning kriteriya bo'yicha natijasi
            
            for i in range(f_num, f_num * 2):                  # Misol uchun 100-999 gacha interval
                check_number, arr = self.checkNumberInIndexes(i, l, indexes[:-1])
                
                if check_number:
                    interval_array = []
                    # print(arr)
                    interval_array.append([sorted_indexes[arr[0] - 1], sorted_indexes[arr[1] - 1]])
                    last_j = arr[1] - 1
                    
                    for j in range(1, l-1):
                        last_j = arr[j+1] - 1
                        interval_array.append([sorted_indexes[arr[j] - 1], sorted_indexes[last_j]])
                    interval_array.append([sorted_indexes[last_j], sorted_indexes[indexes[-1] - 1]])
                    # print(interval_array)
                    criterian_by_col.append([self.colculateCriteria(deter_2D, interval_array), interval_array])
                    # print(criterian_by_col)
                    # criterian_by_col.append([self.colculateCriteria(deter_2D, interval_array), f'{sorted_data[0, c]}___{sorted_data[interval_array[0][-1], c]}__{sorted_data[-1, c]}'])
            # break
            # [print(criterian_by_col[f]) for f in range(len(criterian_by_col))]
            # break
            criterian_all_cols.append(criterian_by_col[self.getMaxCriterianAndInterval(criterian_by_col)])
            # break
        # [print(criterian_all_cols[f]) for f in range(len(criterian_all_cols))]
        # Natijalar:
        criterian_all_cols = sorted(criterian_all_cols, key=lambda x: x[0])[::-1]
        # print()
        [print(criterian_all_cols[f]) for f in range(len(criterian_all_cols))]
       
data = np.loadtxt('datasets/gipertoniyya.txt')
obj = firstCriterian(data)
obj.mainFun()