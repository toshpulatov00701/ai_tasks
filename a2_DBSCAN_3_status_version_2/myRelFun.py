# Faqat butun sonlarda va 1, 2, 3 qiymatlarda bo'lishi kerak va faqat bitta alomatga ega bo'lgan data
import numpy as np
class relatedFunction:
    real_data = None       # Data'ning eng boshida berilgan holati
    changed_data = None    # Alomatlarini formula orqali akslantirilgan ko'rinishi
    
    def __init__(self, data):
        if(self.checkData(data)):
            self.real_data = data
        else:
            print('Nominal alomatlarning mumkin bo\'lgan qiymatlari(gradatsiyalari) chegaradan chiqib ketdi.')
        self.K1relatedFun()

    def checkData(self, data):
        count_objs = len(data)
        if count_objs / 2 < len(np.unique(data)):
            return False
        return True
    
    def K1relatedFun(self):      # Ikkinchi sinf ideal holat uchun olinganda. K2 mavjud bo'lmagan holat uchun
        data = self.real_data
        rows = len(data)
        new_data = np.zeros_like(data, dtype=float)
        for u in range(1, 4):  # 1, 2, 3 - statuslar bo'lgani uchun
            indexes_u = np.where(data == u)
            d_u = np.sum(data == u)
            new_data[indexes_u] = (d_u / rows) / (d_u / rows + 1/3)
        self.changed_data = new_data      

    # def K1relatedFun(self):       # Birdan turg'unligini hisoblab ketish. # K2 mavjud. Lekin ||K1||=||K2||.
    #     delta_data = self.real_data
    #     rows, cols = delta_data.shape
    #     unique_labels = np.unique(delta_data[:,-1])
    #     features = np.zeros(cols - 1)
    #     for i in range(cols - 1):
    #         feature_sum = 0
    #         unique_items = np.unique(delta_data[:,i])        
    #         for j in range(len(unique_items)):
    #             indexes_K_1_u = np.where((delta_data[:, i] == unique_items[j]) & (delta_data[:, -1] == unique_labels[0]))
    #             indexes_K_2_u = np.where((delta_data[:, i] == unique_items[j]) & (delta_data[:, -1] == unique_labels[1]))
    #             d_1_u = len(indexes_K_1_u[0])
    #             d_2_u = len(indexes_K_2_u[0])
    #             f_i_u = d_1_u / (d_1_u + d_2_u)
    #             if f_i_u >= 0.5:
    #                 feature_sum += d_1_u
    #             else:
    #                 feature_sum += d_2_u
    #         features[i] = feature_sum / rows
    #     return features

    def stabilityFeatures(self):  # Turg'unlik hisoblash. 
        data = self.changed_data
        rows = len(data)
        sum_col = 0
        for i in range(rows):
            if data[i] >= 0.5:
                sum_col += data[i]
            else:
                sum_col += 1 - data[i]
        features = sum_col / rows
        return features