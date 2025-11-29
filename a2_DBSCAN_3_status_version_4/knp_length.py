import numpy as np
from distance_metrics import DistMetrics

class KNP(DistMetrics):
    def __init__(self, data, metric_type, normal_type=None):
        super().__init__(data, metric_type, normal_type)

    def find_closer(self, tree_dict, sum_length, re_d_matrix):
        dict_keys = list(tree_dict.keys())

        min_value = np.inf
        closer_node = -1
        new_node = -1

        for key in dict_keys:
            col_index = np.argmin(re_d_matrix[key])
            value = re_d_matrix[key][col_index]

            if value < min_value:
                min_value = value
                closer_node = key         # daraxtdan tugun
                new_node = col_index      # daraxtga qo‘shiladigan tugun

        if self.metric_type == 'euclidean':
            sum_length += np.sqrt(min_value)
        else:
            sum_length += min_value

        for key in dict_keys:
            re_d_matrix[key, new_node] = np.inf
            re_d_matrix[new_node, key] = np.inf

        return closer_node, new_node, sum_length, re_d_matrix


    def get_sum_distances(self):
        if self.m == 1:
            return 0

        re_d_matrix = np.copy(self.distance_matrix)
        re_d_matrix[re_d_matrix == 0] = np.inf

        min_index = np.argmin(re_d_matrix)
        row, col = np.unravel_index(min_index, re_d_matrix.shape)
        min_value = re_d_matrix[row, col]

        if self.metric_type == 'euclidean':
            sum_length = np.sqrt(min_value)
        else:
            sum_length = min_value

        re_d_matrix[row, col] = np.inf
        re_d_matrix[col, row] = np.inf

        tree_dict = dict()
        tree_dict[row] = {col}
        tree_dict[col] = set()

        while len(tree_dict) < self.m:
            closer_node, new_node, sum_length, re_d_matrix = \
                self.find_closer(tree_dict, sum_length, re_d_matrix)

            tree_dict[closer_node].add(new_node)
            tree_dict[new_node] = set()

        return sum_length


# data = np.loadtxt('datasets/wine_1_new.txt', dtype=float)
# metric_type='euclidean'
# normal_type='normalization'

# obj = KNP(data, metric_type='euclidean') 
# print(obj.get_sum_distances())

# sum_k = 0
# for i in range(1):
#     # print(i)
#     data = np.loadtxt(f'datasets/claster-data/2-{8}-klaster.txt', dtype=float)
#     obj = KNP(data, metric_type='euclidean', normal_type='normalization')
#     sum_k += obj.get_sum_distances() 
#     print(obj.get_sum_distances())
# print('sum_k:', sum_k)