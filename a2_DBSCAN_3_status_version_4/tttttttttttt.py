import matplotlib.pyplot as plt

# ---------------------------
# 1. DATA ro'yxati
# ---------------------------
points = [
(57,47),(59,72),(46,46),(73,61),(42,58),(43,43),(53,21),(24,41),(34,54),(36,28),
(71,46),(51,28),(41,51),(32,55),(40,45),(40,77),(49,34),(62,31),(53,20),(30,52),
(61,52),(48,45),(27,39),(43,65),(55,23),(54,44),(39,59),(65,63),(37,45),(54,64),
(42,47),(33,32),(62,70),(48,65),(55,40),(55,73),(49,73),(10,62),(51,45),(51,20),
(46,55),(72,42),(37,42),(63,54),(42,57),(51,64),(39,45),(44,28),(54,53),(50,46),
(28,43),(44,37),(47,56),(78,52),(53,48),(21,49),(50,86),(47,54),(49,32),(67,61),
(61,36),(71,28),(58,82),(35,41),(51,42),(26,51),(34,57),(36,73),(38,45),(62,31),
(53,69),(25,52),(53,61),(31,30),(57,54),(53,55),(39,53),(54,39),(77,57),(32,59),
(35,61),(67,37),(64,56),(62,78),(46,38),(36,37),(48,55),(54,62),(50,71),(46,90),
(59,37),(33,57),(46,60),(57,48),(37,27),(43,62),(53,31),(52,55),(36,52),(50,32)
]

# Koordinatalarni massivga ajratish
xs = [p[0] for p in points]
ys = [p[1] for p in points]

# ---------------------------
# 2. Cluster indexlari
# ---------------------------

# 1-BOSQICH
b1_c1 = [ 2,4,5,8,12,13,14,19,20,21,23,25,26,28,30,34,38,40,42,44,46,48,49,52,54,57,63,64,65,66,68,71,74,75,76,77,79,80,85,86,90,91,92,93,95,97,98 ]
b1_c2 = [16,58,84,96,99]
b1_c3 = [29,33,45,70,72,87]

# 2-BOSQICH
b2_c1 = [1,3,10,15,17,27,32,35,36,41,43,53,56,59,60,61,62,67,69,78,81,82,83,88,89]
b2_c2 = [6,11,18,24,39]
b2_c3 = [9,31,47,73,94]

# Anomallar
anom = [0,7,22,37,50,51,55]

# ---------------------------
# 3. Chizish funksiyasi
# ---------------------------

def draw_cluster(indices, color, marker, label):
    for idx in indices:
        plt.scatter(xs[idx], ys[idx], c=color, marker=marker, s=70, label=label)
        label = None  # legend takrorlanmasligi uchun

# ---------------------------
# 4. CHIZISH
# ---------------------------
plt.figure(figsize=(7,7))
# plt.grid(True)

# 1-bosqich — marker = o
draw_cluster(b1_c1, 'blue', 'o', '1-bosqich 1-klaster')
draw_cluster(b1_c2, 'green', 'o', '1-bosqich 2-klaster')
draw_cluster(b1_c3, 'orange', 'o', '1-bosqich 3-klaster')

# 2-bosqich — marker = s
draw_cluster(b2_c1, 'cyan', 's', '2-bosqich 1-klaster')
draw_cluster(b2_c2, 'lime', 's', '2-bosqich 2-klaster')
draw_cluster(b2_c3, 'purple', 's', '2-bosqich 3-klaster')

# Anomallar — X marker
draw_cluster(anom, 'red', 'X', 'Anomallar')

plt.title("2D: Bosqichlar va klasterlar bilan tasvir", fontsize=15)
plt.xlabel("X")
plt.ylabel("Y")
plt.legend(loc='best', fontsize=9)
plt.show()
