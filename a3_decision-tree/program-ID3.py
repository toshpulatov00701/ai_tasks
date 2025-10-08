import math

def getUniques(data, lab_uniques, col_index):
    unique_result = []
    uniques = []
    for delta in data:
        if not(delta[col_index] in uniques):
            uniques.append(delta[col_index])
            count_item, lab_arr, class_name = checkLastCol(data, lab_uniques, col_index, delta[col_index])
            unique_result.append([delta[col_index], lab_arr, count_item, class_name])
    return unique_result

def checkLastCol(data, lab_uniques, col_index, item):    # unique col item keladi. Kelyotgan item bir sinfga tegishli bo'lsa o'sha sinfni, aks holda 'noaniq' deb javob qaytadi
    new_data = [row for row in data if row[col_index] == item]
    label_data = [row[-1] for row in new_data if row[-1] == new_data[0][-1]]

    last_col = [row[-1] for row in new_data]
    lab_arr = []
    for l in lab_uniques:
        lab_arr.append(last_col.count(l))
    if len(new_data) == len(label_data):
        return len(new_data), lab_arr, new_data[0][-1]
    else:
        return len(new_data), lab_arr, 'noaniq'

def computeIG(data, col_index, lab_uniques):
    u_labels = getUniques(data, lab_uniques, len(data[0])-1)
    count_row = sum([row[-2] for row in u_labels])
    H = 0
    for l in u_labels:
        H += (l[-2] / count_row) * math.log2(l[-2]/count_row)
    H *= -1
    HS = []
    u_col = getUniques(data, lab_uniques, col_index)
    for item in u_col:
        p = 0
        count_r = item[-2]
        for s in item[1]:
            if s != 0:
                p += (s / count_r) * math.log2(s/count_r)
        p *= -1
        HS.append([p, item[-2]])
    p = 0
    for h in HS:
        p += (h[-1] / count_row) * h[0]
    p *= -1
    H += p
    return H

def findMaxGI(all_GI):
    max_val = all_GI[0][0]
    delta_GI = all_GI[0]
    for gi in all_GI:
        if max_val < gi[0]:
            max_val = gi[0]
            delta_GI = gi
    return delta_GI

def mainFun(data, attributes, lab_uniques):
    all_GI = []
    for i in range(len(attributes)):
        all_GI.append([computeIG(data, i, lab_uniques), i])
    maxGI = findMaxGI(all_GI)
    u_col = getUniques(data, lab_uniques, maxGI[-1])
    # print('u_col:\n',u_col)
    # print('prev data: \n', data)

    check_attr = []
    for row in data:
        check_attr.append(row[-1])
    if check_attr.count(check_attr[0]) == len(data):
        return check_attr[0]
    new_attr = [attributes[i] for i in range(len(attributes)) if i != maxGI[-1]]
    tree = {} 
    for u in u_col:
        new_data = []
        checker = []
        for row in data:
            if row[maxGI[-1]] == u[0]:
                row.pop(maxGI[-1])
                new_data.append(row)
                checker.append(row[-1])
        # print('new data:\n', new_data)
        # print('attr:\n', new_attr)  
        tree[u[0]] = mainFun(new_data, new_attr, lab_uniques)
    return {attributes[maxGI[-1]]: tree}

attributes = ["Havo", "Harorat", "Namlik", "Shamol"]
data = [
    ["Quyoshli",  "Issiq", "Yuqori", "Kuchsiz", "Yoq"],
    ["Quyoshli",  "Issiq", "Yuqori", "Kuchli", "Yoq"],
    ["Bulutli",   "Issiq", "Yuqori", "Kuchsiz", "Ha"],
    ["Yomgirli", "Iliq",  "Yuqori", "Kuchsiz", "Ha"],
    ["Yomgirli", "Sovuq", "Normal", "Kuchsiz", "Ha"],
    ["Yomgirli", "Sovuq", "Normal", "Kuchli", "Yoq"],
    ["Bulutli",   "Sovuq", "Normal", "Kuchli", "Ha"],
    ["Quyoshli",  "Iliq",  "Yuqori", "Kuchsiz", "Yoq"],
    ["Quyoshli",  "Sovuq", "Normal", "Kuchsiz", "Ha"],
    ["Yomgirli", "Iliq",  "Normal", "Kuchsiz", "Ha"]
]

lab_uniques = []
for row in data:
    if not(row[-1] in lab_uniques):
        lab_uniques.append(row[-1])

# print(getUniques(data, lab_uniques, len(data[0])-1))
print(mainFun(data, attributes, lab_uniques))
