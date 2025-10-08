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
        _, count_features = delta_data.shape
        unique_labels = np.unique(delta_data[:,-1])
        K_1 = len(np.where(delta_data[:,-1] == unique_labels[0])[0])
        K_2 = len(delta_data[:,-1]) - K_1
        
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
        # last_row_str = 25
        # last_row_str = ['%g'] * 25
        last_row_str = ['%g'] * 4
        print(new_data)
        np.savetxt('re-meteo1111111.dat', new_data, fmt=last_row_str)
        self.changed_data_2 = new_data
    
    def separateByClass(self):
        delta_data = self.changed_data_2
        features = np.zeros((len(delta_data[0]) - 1))
        unique_labels = np.unique(delta_data[:,-1])
        for col in range(len(delta_data[0]) - 1):
            t = 0
            for i in range(len(delta_data)):
                if (delta_data[i, col] > 0.5) & (delta_data[i, -1] == unique_labels[0]):
                    t += 1
                if (delta_data[i, col] < 0.5) & (delta_data[i, -1] == unique_labels[1]):
                    t += 1
            features[col] = 100 - ((len(delta_data) - t) * 100)/ len(delta_data)
        print(features)
        print('Max index: ', np.argmax(features))

# data = np.loadtxt('uzbkares.txt', dtype=float)
# myobj = relatedFunction(data)
# myobj.K1relatedFun()
# myobj.separateByClass()