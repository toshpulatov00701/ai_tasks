import numpy as np

class priorityInter():
    data = None     
    array_K = None  # Har bir sinf va ularning soni

    def __init__(self, data):
        self.array_K = np.unique_counts(data[:,-1])
        self.data = data
        
    def sortArray(self, arr): # Shu ko'rinishda tartiblash zarur. Negaki bir xil kelib qolgan alomatlarning sinflari tartibi hom alomat tartibida kelishi kerak.
        for i in range(len(arr)):
            for j in range(i+1, len(arr)):
                if arr[i,0] > arr[j, 0]:
                    delta = np.copy(arr[i]) 
                    arr[i] = arr[j]
                    arr[j] = delta
        return arr
    
    def byAllInterval(self, sorted_col): # Tartiblangan alomat qiymatlarining har bir intervalida qaysi sinf ustunlik qilyotganligini hisoblash
        K_1 = self.array_K[1][0]
        K_2 = self.array_K[1][1]
        res_K = None                     # Qaysi sinf ustunlik qilyotgani va necha % tashkil etishi
        res_criterian_max = -1
        res_i, res_j = 0, 0
        for i in range(len(sorted_col)):
            for j in range(i+1, len(sorted_col)+1):
                d1 = np.sum(sorted_col[i:j, 1] == int(self.array_K[0][0]))
                d2 = np.sum(sorted_col[i:j, 1] == int(self.array_K[0][1]))
                res_criterian = np.abs( d1 / K_1 - d2 / K_2 )
                if res_criterian > res_criterian_max:
                    res_criterian_max = res_criterian
                    res_i = i
                    res_j = j

                    if d1 > d2: 
                        res_K = ('K1', (d1 * 100/ (d1 + d2)))
                    elif d1 < d2: 
                        res_K = ('K2', (d2 * 100/ (d1 + d2)))
                    else: 
                        res_K = ('K1==K2', 50)
        
        res_string = f'{int(sorted_col[res_i, -1]), int(sorted_col[res_j-1, -1])} \t criteriya qiymati: {res_criterian_max}  \t{res_K[0]}({res_K[1]}%)\n'
        if res_i == 0 and res_j == len(sorted_col):
            return res_string
        if res_i == 0:
            return res_string + self.byAllInterval(sorted_col[res_j:,:])
        if res_j == len(sorted_col):
            return self.byAllInterval(sorted_col[:res_i,:]) + res_string
        return self.byAllInterval(sorted_col[:res_i,:]) + res_string + self.byAllInterval(sorted_col[res_j:,:])

    def mainFun(self):
        data = self.data
        _, cols = np.shape(data)
        for c in range(cols-1):
            sorted_col = self.sortArray(data[:,[c, -1]])
            col_indexes = np.array([range(len(sorted_col))]).reshape(len(sorted_col), 1)
            res_col = np.hstack((sorted_col, col_indexes))
            print(f'********-- {c+1} - alomat uchun --********')
            print(self.byAllInterval(res_col))
            
data = np.loadtxt('datasets/testdata-2.txt')
p = priorityInter(data)
p.mainFun()