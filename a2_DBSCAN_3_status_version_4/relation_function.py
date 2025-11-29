# Faqat butun sonlarda va 1, 2 qiymatlarda bo'lishi kerak va faqat bitta alomatga ega bo'lgan va harakteristik vektori bo'lmagan data.
import numpy as np
class RelatedFunction:

    def __init__(self, data, anomal_percent):
        self.anomal_percent = anomal_percent      # Anomallar %da [0, 100]
        
        if(self.check_data(data)):
            self.data = data.astype(int)          # Bitta alomatga ega bo'lgan data
        else:
            raise ValueError("Data faqat bitta alomatli bo'lishi, butun sonlardan iborat bo'lishi va qiymatlar faqat {1, 2} bo'lishi kerak. Nominal alomatlarning mumkin bo'lgan gradatsiyalari chegarasidan chiqib ketdi.")

    def check_data(self, data):
        count_objs = len(data)
        uniq_items = np.unique(data)

        if data.ndim != 1:                            # Bir o'lchamli bo'lsin
            return False
        
        if count_objs / 2 < len(uniq_items):
            return False
        
        if not np.all(np.isin(uniq_items, [1, 2])):   # Faqat 1, 2 dan iborat
            return False
        
        return True
    
    def stability_features(self):                     # Ikkinchi sinf mavjud emas. Biroq miqdori beriladi.
        data = self.data
        anomal_percent = self.anomal_percent
        rows = len(data)

        d_v = np.array([(100 - anomal_percent) / 100, anomal_percent / 100])            #  d(v) = [normal ulushi, anomallar ulushi] 
        sum_gc = 0
        for u in (1, 2):                                                                # 1, 2 - statuslar bo'lgani uchun. 2 - anomal, 1 - yadroviy va chegaraviy
            d_u = np.sum(data == u)
            d1_c_u = d_u / rows 
            
            fc_u = d1_c_u / (d1_c_u + d_v[u - 1])
            
            if fc_u >= 0.5:
                sum_gc += d1_c_u
            else:
                sum_gc += d_v[u - 1]
        return sum_gc / 2

# arr = np.array([1, 1, 2, 1, 2, 2, 1, 1])
# objRelFun = RelatedFunction(arr, 40)
# print(objRelFun.stability_features())