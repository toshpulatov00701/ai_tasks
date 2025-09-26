import numpy as np
class EstimationAlgorithm:           
    accuracy = None
    precision = None
    recall = None
    f1_score = None
    def __init__(self, correct_answer, alg_result, pos_label = 1):
        self.setAtributes(correct_answer, alg_result, pos_label)

    def setAtributes(self, correct_answer, alg_result, pos_label):
        count_objs = len(correct_answer)
        real_normal = np.sum(correct_answer == 1)
        real_anomal = count_objs - real_normal
        alg_normal = np.sum(alg_result == 1)
        alg_anomal = count_objs - alg_normal
        if pos_label == -1:
            t = 0
            for i in range(count_objs):
                if correct_answer[i] == 1 and alg_result[i] == -1:
                    t+=1
            TP = alg_anomal - t                                 # Model topgan anomallar soni
            FP = t                                              # Model anomal deb topganlar ichidagi normallar soni
            TN = real_normal - t                                # Model topgan normallar soni
            FN = real_anomal - TP                               # Model normal deb topganlar ichidagi anomallar soni
        else:
            t = 0
            for i in range(count_objs):
                if correct_answer[i] == -1 and alg_result[i] == 1:
                    t+=1
            TP = alg_normal - t
            FP = t
            TN = real_anomal - t
            FN = real_normal - TP

        self.showEstimatin(TP, FP, TN, FN)

    def showEstimatin(self, TP, FP, TN, FN):

        accuracy = (TP + TN) / (TP + FP + TN + FN)
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        f1_score = 2 * (precision * recall) / (precision + recall)
        
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1_score = f1_score
    
    def showAllParametr(self):
        print('Accuracy:', self.accuracy)
        print('Precision:', self.precision)
        print('Recall:', self.recall)
        print('F1-score:', self.f1_score)

# -1 - anomal, 1 - normal

# real_data = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1])
# alg_data = np.array([1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, -1, -1])

# obj = EstimationAlgorithm(real_data, alg_data, -1) # -1 nimaga nisbatan ekanligi(1 - normal, -1 - anomal)