# Faqat butun sonlarda va 1, 2 qiymatlarda bo'lishi kerak va faqat bitta alomatga ega bo'lgan data
import numpy as np
class relatedFunction:
    real_data = None       # Data'ning eng boshida berilgan holati
    changed_data = None    # Alomatlarini formula orqali akslantirilgan ko'rinishi
    
    def __init__(self, data, anomal_percent):
        if(self.checkData(data)):
            self.real_data = data
        else:
            print('Nominal alomatlarning mumkin bo\'lgan qiymatlari(gradatsiyalari) chegaradan chiqib ketdi.')
        self.K1relatedFun(anomal_percent)

    def checkData(self, data):
        count_objs = len(data)
        if count_objs / 2 < len(np.unique(data)):
            return False
        return True
    
    def K1relatedFun(self, anomal_percent):      # Ikkinchi sinf ideal holat uchun olinganda. K2 mavjud bo'lmagan holat uchun
        data = self.real_data
        rows = len(data)
        new_data = np.zeros_like(data, dtype=float)
        d_v_array = np.array([(100 - anomal_percent) / 100, anomal_percent / 100])
        for u in range(1, 3):  # 1, 2 - statuslar bo'lgani uchun
            indexes_u = np.where(data == u)
            d_u = np.sum(data == u)
            new_data[indexes_u] = np.round((d_u / rows) / (d_u / rows + d_v_array[u - 1]), 5)
        self.changed_data = new_data      

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