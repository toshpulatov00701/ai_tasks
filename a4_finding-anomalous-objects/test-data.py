import numpy as np
import anomDetHyperSpere

obj = anomDetHyperSpere.buildHyperSpere(55)

print(obj.r)


# arr = np.array([[1, 2], [3, 4]])
# a = np.array([1, 1])
# print(np.linalg.norm((arr - a), axis=1))
# print(a + arr)


# 1 - test
S = np.array([
    [1, 2, 1],
    [5, 4, 3],
    [3, 5, 1],
    [8, 4, 1],
    [6, 3, 3],
    [6, 4, 1],
    [7, 5, 1],
    [8, 8, 1],
    [4, 5, 3],
    [10, 10, 1],
    [10, 8, 1],
    [11, 10, 3],
    [11, 9, 3],
    [7, 7, 3],
    [1, 1, 0]
])


# 2 - test
S = np.array([
        [80, 100, 32, 12, 30],
        [76, 200, 28, 14, 30],
        [84, 200, 30, 10, 60],
        [ 5, 100, 99, 90, 60],
        [82, 100, 30,  8, 60],
        [ 1,   0,  1,  1,  0]
])

# 3 - test
S = np.array([
        [1, 100, 2, 30],
        [25, 200, 24, 30],
        [39, 100, 31, 60],
        [2, 200, 5, 60],
        [4, 200, 2, 30],
        [4, 100, 5, 60],
        [7, 100, 3, 30],
        [1, 200, 8, 60],
        [4, 200, 8, 60],
        [9, 100, 3, 30],
        [21, 100, 20, 60],
        [22, 100, 20, 60],
        [8, 200, 1, 60],
        [ 1,   0,  1,  0]
])

# 4 - test
S = np.empty((101, 6), dtype=int) # 100x6 matritsa, 90 normal, 10 ta anomal
class_name = 70
for i in range(90):
    if i % 3 == 0:
        class_name = 75
    else:
        class_name = 70
    S[i] = [
        np.random.randint(10, 30),
        np.random.randint(50, 70),
        np.random.randint(100, 130),
        np.random.randint(400, 500),
        np.random.randint(2000, 2500),
        class_name
    ]
for i in range(90, 100):
    if i % 4 == 0:
        class_name = 75
    else:
        class_name = 70
    S[i] = [
        np.random.randint(10, 30),
        np.random.randint(250, 270),
        np.random.randint(700, 830),
        np.random.randint(600, 800),
        np.random.randint(2000, 2500),
        class_name
    ]
S[100] = [1, 1, 1, 1, 1, 0]

# 5 - test
S = np.loadtxt("meteo-easy.dat", dtype=float)



