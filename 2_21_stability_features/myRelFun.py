import numpy as np
class relatedFunction:
    real_data = None    # Data'ning eng boshida berilgan holati
    changed_data = None # Alomatlarini 1, 2, 3 v.h larda tasvirlangani. Maqsodiga
    changed_data_2 = None # Alomatlarini formula orqali akslantirilgan ko'rinishi
    
    def __init__(self, data):
        if(self.checkData(data)):
            self.real_data = data
            self.changed_data = self.primaryProcessing(data)
        else:
            print('Nominal alomatlarning mumkin bo\'lgan qiymatlari(gradatsiyalari) chegaradan chiqib ketdi.')
        
    def checkData(self, data):
        count_objs, count_features = data.shape
        for i in range(count_features - 1):
            if count_objs / 2 < len(np.unique(data[:,i])):
                return False
        return True
    
    def primaryProcessing(self, data):
        _, count_features = data.shape
        delta_data = np.zeros_like(data, dtype=int)
        for i in range(count_features - 1):
            _, encoded = np.unique(data[:, i], return_inverse=True)
            delta_data[:, i] = encoded + 1      
        delta_data[:, -1] = data[:, -1]
        return delta_data
    
    def K1relatedFun(self):
        delta_data = self.changed_data
        count_obj, count_features = delta_data.shape
        unique_labels = np.unique(delta_data[:,-1])
        K_1 = np.sum(delta_data[:, -1] == unique_labels[0])
        K_2 = count_obj - K_1
        new_data = np.zeros_like(delta_data, dtype=float)

        for i in range(count_features - 1):
            unique_items = np.unique(delta_data[:,i])        
            for j in range(len(unique_items)):
                indexes_K_1_u = np.where((delta_data[:, i] == unique_items[j]) & (delta_data[:, -1] == unique_labels[0]))
                indexes_K_2_u = np.where((delta_data[:, i] == unique_items[j]) & (delta_data[:, -1] == unique_labels[1]))
                d_1_u = len(indexes_K_1_u[0])
                d_2_u = len(indexes_K_2_u[0])
                f_i_u = np.round((d_1_u / K_1) / ((d_1_u / K_1) + (d_2_u / K_2)), 2)
                new_data[indexes_K_1_u, i] = f_i_u
                new_data[indexes_K_2_u, i] = f_i_u
        new_data[:, -1] = delta_data[:, -1] 
        self.changed_data_2 = new_data
    
    def stabilityFeatures(self):  # Turg'unlik hisoblash
        delta_data = self.changed_data_2
        [print(delta_data[i]) for i in range(len(delta_data))]
        rows, cols = np.shape(delta_data)
        features = np.zeros((cols - 1))
        for col in range(cols - 1):
            sum_col = 0
            for i in range(rows):
                if delta_data[i, col] >= 0.5:
                    sum_col += delta_data[i, col]
                elif delta_data[i, col] < 0.5:
                    sum_col += 1 - delta_data[i, col]
            features[col] = sum_col / rows

        desc_sort = np.sort(features)[::-1]
        desc_sort_index = np.argsort(-features) + 1
        print('Alomat \t-- \tTurg\'unlik')
        for item in range(len(desc_sort)):
            print(f'{desc_sort_index[item]} \t-- \t{desc_sort[item]}')

data = np.loadtxt('uzbkares.txt', dtype=float)
myobj = relatedFunction(data)
myobj.K1relatedFun()
myobj.stabilityFeatures()