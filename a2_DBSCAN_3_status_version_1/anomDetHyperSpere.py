import numpy as np

class buildHyperSpere:
    data = None     # Data'ning ohirgi ustuni olib tashlangani
    C = None             # Markaz
    r = None             # Gipershar radiusi
    lambda_reg = None    # Regularizatsiya parametri
    
    def __init__(self, data, lambda_reg = 1):
        self.lambda_reg = lambda_reg
        self.data = data[:,:-1]    
    
    def euiclidenDistances(self, data, C):            # Markaz va boshqa obyektlar o'rtasidagi masofalar
        return np.linalg.norm(data - C, axis=1)

    def computeRadius(self, data, C):
        return np.mean(self.euiclidenDistances(data, C))
    
    def computeCenter(self, data, C, r):
        inner_objects = self.euiclidenDistances(data, C) <= r
        data_in = data[inner_objects]
        if len(data_in) == 0:
            return C
        return np.mean(data_in, axis=0)

    
    def lossFunction(self, data, C, r):
        lambda_reg = self.lambda_reg
        distances = self.euiclidenDistances(data, C)
        loss = np.sum(r**2 - distances**2)
        loss = np.clip(loss, -100, 100)
        return lambda_reg * (r**2) + (-1) * loss

    def findHyperspere(self, tol = 1e-6, itar = 100):
        data = self.data
        delta_C = np.mean(data, axis=0)
        delta_r = np.mean(self.euiclidenDistances(data, delta_C))
        prev_obj_value = float('inf')
        for i in range(itar):
            delta_C = self.computeCenter(data, delta_C, delta_r)
            delta_r = self.computeRadius(data, delta_C)
            obj_value = self.lossFunction(data, delta_C, delta_r)
            if prev_obj_value - obj_value <= tol:
                break
            prev_obj_value = obj_value
        self.C = delta_C
        self.r = delta_r
    
    def centerObjIndex(self):   # Markazga yaqin obyektni topish
        data = self.data
        C = self.C
        distance_C_obj = self.euiclidenDistances(data, C)
        res_obj_index = np.argsort(distance_C_obj)[0] 
        return res_obj_index