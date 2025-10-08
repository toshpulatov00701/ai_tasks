import numpy as np
class buildClosenessMatrix:
    data = None
    def __init__(self, data):
        self.data = data
        
    def calculate_g(self, a, b, i, j):
        data = self.data
        result = None
        if (data[a, i] == data[b, i]) and (data[a, j] == data[b, j]):
            result = 0
        elif (data[a, i] == data[b, i]) or (data[a, j] == data[b, j]):
            result = 1
        elif (data[a, i] != data[b, i]) and (data[a, j] != data[b, j]):
            result = 2
        return result
    
    def calculate_a(self, a, b):
        data = self.data
        if data[a, -1] == data[b, -1]:
            return 0
        return 1
    
    def calculate_b(self):
        data = self.data
        m, n = np.shape(data)
        n -= 1                                   # Alomatlar soni
        b_matrix = np.ones((n, n)) * (-1)
        K_arrays = np.unique_all(data[:, -1])[3]
        denominator = 0
        for u in range(len(K_arrays)):
            denominator += K_arrays[u] * (m - K_arrays[u])
        denominator *= 2

        for i in range(n):
            for j in range(i, n):
                if i != j:
                    sum_outer = 0
                    for a in range(m):
                        sum_inner = 0
                        for b in range(m):
                            sum_inner += self.calculate_a(a, b) * self.calculate_g(a, b, i, j)
                        sum_outer += sum_inner / denominator
                    b_matrix[i, j] = sum_outer
                    b_matrix[j, i] = sum_outer
                else:
                    b_matrix[i, j] = 0
        return b_matrix
    def sortedPairFeature(self):
        b_matrix = self.calculate_b()
        print(b_matrix)
        arr_length = len(b_matrix) * len(b_matrix[0])
        result = []
        while np.sum(b_matrix == 0) != arr_length:
            row_i, col_i = np.unravel_index(np.argmax(b_matrix), b_matrix.shape)
            b_matrix[row_i,:] = 0
            b_matrix[:,col_i] = 0
            b_matrix[col_i,:] = 0
            b_matrix[:,row_i] = 0
            result.append([int(row_i), int(col_i)])

        print('Informativ alomatlar juftligi: ', result)

data = np.loadtxt('datasets/uzbkares.txt', dtype=int)
obj = buildClosenessMatrix(data)
obj.sortedPairFeature()