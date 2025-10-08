import numpy as np
from anomDetHyperSpere import buildHyperSpere
from myRelFun import relatedFunction

# data = np.loadtxt("meteo.dat") # Harakteristik vektorga ega bo'lgan, real berilganlar

# objSpere = buildHyperSpere(data)
# objSpere.findHyperspere()
# objSpere.findAnomalouses()
# # objSpere.eDensity(3, 1)
# # objSpere.anomalNormalPercent()
# # objSpere.eachOtherDistances()
# objSpere.setLabel()

#************** K tegislilik funksiyasi asosida informativ alomatlarni aniqlash[faqat nominallarda] *************************

# data = np.loadtxt('re-meteo-test.dat', dtype=float)
# [print(data[i]) for i in range(len(data))]
data = np.loadtxt('re-meteo.dat', dtype=float)

# nominal datani ajratib olish
last_row = data[-1, :]
nominal_features = np.argwhere(last_row == 0)
nominal_features = nominal_features.reshape(len(nominal_features))
nominal_data = data[0:-1, nominal_features]
[print(nominal_data[i]) for i in range(len(nominal_data))]
myobj = relatedFunction(nominal_data)
myobj.K1relatedFun()
myobj.separateByClass()

# print(nominal_data)
# print(nominal_features)


