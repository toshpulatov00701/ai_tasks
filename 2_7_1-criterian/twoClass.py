# Ushbu yechim 1-kriteriyaning hususiy yechimi(faqat 2 ta sinf uchun) hisoblanadi. Unga berilishi kerak bo'lgan dataset - faqat miqdoriy, oxirgi ustuni sinf nomi nominal
import numpy as np

class firstCriterian:
    K_arrays = None       # Sinflar va ularning mos soni
    data = None           # Dastlabki dataset
    def __init__(self, data):
        self.data = data
        self.set_K()

    def set_K(self):
        delta_data = self.data
        unique_items = np.unique_counts(delta_data[:,-1])
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
        unique_indexes = np.append(unique_indexes, len(sorted_col) - 1)
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
        for i in range(2):
            res_sum += delta_K_arrays[1][i] * (m - delta_K_arrays[1][i])
        return res_sum 

    def rightNumerator(self, deter_2D, interval_array): # o'ng surat
        delta_K_arrays = self.K_arrays
        m = np.sum(delta_K_arrays[1])
        s_outer = 0
        for p in range(2):
            sum_u_j_p = np.sum(deter_2D[:, interval_array[p][1]] - deter_2D[:, interval_array[p][0]])
            s_inner = 0
            for i in range(2):
                u_i_p = deter_2D[i, interval_array[p][1]] - deter_2D[i, interval_array[p][0]]
                s_inner += u_i_p * (m - delta_K_arrays[1][i] - sum_u_j_p + u_i_p)
            s_outer += s_inner
        return s_outer
        
    def leftDenominator(self): # chap maxraj
        delta_K_arrays = self.K_arrays
        res_sum = 0
        for i in range(2):
            res_sum += delta_K_arrays[1][i] * (delta_K_arrays[1][i] - 1)
        return res_sum 

    def leftNumerator(self, deter_2D, interval_array): # chap surat
        s_outer = 0
        for p in range(2):
            s_inner = 0
            for i in range(2):
                u_i_p = deter_2D[i, interval_array[p][1]] - deter_2D[i, interval_array[p][0]]
                s_inner += (u_i_p - 1) * u_i_p
            s_outer += s_inner
        return s_outer

    def getMaxCriterianAndInterval(self, arr):
        max_item = -1
        j = -1
        for i in range(len(arr)):
            if max_item < arr[i][-1]:
                j = i
                max_item = arr[i][-1]
        return j

    def mainFun(self):
        delta_data = self.data
        _, cols = np.shape(delta_data)
        criterian_all_cols = []
        for c in range(0, cols-1):
            sorted_data = data[data[:, c].argsort()] 
            su_indexes = self.getColSortedIndex(sorted_data[:,c])                             # tartiblangan va unikal bo'lgan qiymatlar
            deter_2D = self.buildDeter2D(sorted_data[:, -1])
            criterian_by_col = []
            for h in range(1, len(su_indexes) - 1):
                interval_array = [[0, su_indexes[h]], [su_indexes[h], su_indexes[-1] + 1]]    # mumkin bo'lgan intervallarni qurish
                criterian_val = self.colculateCriteria(deter_2D, interval_array)
                interval_array[1][1] -= 1                                                     # deter_2D orqali hisoblab bolganimizdan song qo'shilgan 1 ni olib tashlaymiz
                c_2 = interval_array[0][1] - 1
                interval_array[0][0] = float(sorted_data[interval_array[0][0],c])
                interval_array[0][1] = float(sorted_data[interval_array[0][1]-1,c])
                interval_array[1][0] = float(sorted_data[interval_array[1][0]-1,c])
                interval_array[1][1] = float(sorted_data[interval_array[1][1],c])
                criterian_by_col.append([c_2, interval_array, criterian_val])
            criterian_all_cols.append(criterian_by_col[self.getMaxCriterianAndInterval(criterian_by_col)])
        criterian_all_cols = sorted(criterian_all_cols, key=lambda x: x[-1])[::-1]
        [print(f'{criterian_all_cols[f][0]} \t {criterian_all_cols[f][1]} \t {criterian_all_cols[f][2]}') for f in range(len(criterian_all_cols))]
       
data = np.loadtxt('datasets/dogwolfdata.txt')
obj = firstCriterian(data)
obj.mainFun()