import numpy as np
import pandas as pd

def qoshmAjratish(qoshimchalar_dict, qolgan_q):    # Qo'shimchalarni ajratish
    qoshimcha_keys = sorted(qoshimchalar_dict.keys(), key=len, reverse=True)
    ajratilgan_q = []
    while qolgan_q:
        found_affix = False
        for q in qoshimcha_keys:
            if qolgan_q.startswith(q):
                value = qoshimchalar_dict[q]                 
                if value is None:
                    ajratilgan_q.append(q)
                    qolgan_q = qolgan_q[len(q):]
                else:
                    for q_sub in value:
                        ajratilgan_q.append(q_sub)
                    qolgan_q = qolgan_q[len(q):]   
                found_affix = True
                break
        if not found_affix:
            print(f"Baza qo'shimchalarida mos keluvchi qo'shimcha topilmadi: '{qolgan_q}'")
            break    
    return ajratilgan_q

def qaytaIshlashTest(test_gap, t_asoslar):   # Berilgan test gapni qayta ishlash. Massivlarga ajratib olish.
    test_gap = test_gap.replace(" ", "")     # Probellarni olib tashlash
    test_gap = test_gap.lower()              # Katta harflarni kichikka o'tkazish
    test_gap_delta = test_gap
    delta_test = ""
    for w in t_asoslar:
        found = test_gap_delta.find(w)
        if found != -1:
            delta_test += ' ' + test_gap_delta[found:(found + len(w))]
            test_gap_delta = test_gap_delta[found + len(w):]
    delta_test = delta_test.strip()
    delta_test = np.array(delta_test.split(' '))

    for d in delta_test:
        test_gap = test_gap.replace(d, " " + d)
    test_gap = test_gap.strip()
    test_gap = np.array(test_gap.split(' '))
    return test_gap

def qaytaIshlashQoshimcha(qoshimchalar):
    qoshimchalar_dict = dict()
    for q_i in range(len(qoshimchalar)):
        if qoshimchalar[q_i, 1] == 'nan':
            qoshimchalar_dict[qoshimchalar[q_i, 0]] = None
        else:
            qoshimchalar_dict[qoshimchalar[q_i, 0]] = np.array(qoshimchalar[q_i, 1].split(' '))
    return qoshimchalar_dict
###########################################################

df = pd.read_csv("sozlar.csv")
asoslar = df.astype(str).to_numpy()

uzunlik = np.vectorize(len)(asoslar[:, 0])
t_asoslar = asoslar[:, 0][np.argsort(-uzunlik)]

test_gap = "maktabimiz      Ajoyibkitoblarining"
test_gap = qaytaIshlashTest(test_gap, t_asoslar)

df = pd.read_csv("qoshimchalar.csv")
qoshimchalar = df.astype(str).to_numpy()
qoshimchalar_dict = qaytaIshlashQoshimcha(qoshimchalar)

for s_i in range(len(test_gap)):
    natija_asos = ""
    ajratilgan_q = []
    s_turkum = ''
    for a_i in range(len(asoslar[:, 0])):
        t_index = test_gap[s_i].find(asoslar[a_i, 0])
        if t_index == 0:
            s_turkum = asoslar[a_i, 1]
            natija_asos = test_gap[s_i][0:len(asoslar[a_i, 0])]
            
            qolgan_q = test_gap[s_i][len(asoslar[a_i, 0]):]
            ajratilgan_q = qoshmAjratish(qoshimchalar_dict, qolgan_q)
            break

    print(f'{s_i + 1} - so\'z uchun: ')
    print(f"Asos: {natija_asos}")
    print(f"So'z turkumi: {s_turkum}")
    print(f"Ajratilgan Qo'shimchalar: {ajratilgan_q}")
    print()