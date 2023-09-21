import re


def readInput():
    with open("data.txt", "r") as data:
        sequence = []
        for lines in data:
            transactions = lines[1:-2]
            parts = transactions.split("}{")
            lists = [part.strip("{}").split(",") for part in parts]
            seq = [[int(item) for item in transact] for transact in lists]
            sequence.append(seq)
        data.close()
    return sequence

sequences = readInput()
NO_OF_SEQUENCES = len(sequences)
MIS = {
    10: 0.45,
    20: 0.30,
    30: 0.30,
    40: 0.45,
    50: 0.45,
    60: 0.30,
    70: 0.30,
    80: 0.30,
    90: 0.30,
    "SDC": 0.1,
    'rest': 0.69
}

def sort_items(I,MIS):
    items_mis = {}
    for item in I:
        items_mis[item] = MIS.get(item, MIS['rest'])
    items_mis = dict(sorted(items_mis.items(), key=lambda item: item[1]))
    return list(items_mis.keys())

def item_actual_support(items,sequences):
    i = {}
    for item in items:
        item_occur = 0
        for seq in sequences:
            for transact in seq:
                if item in transact:
                    item_occur+=1
                    break
        i[item] = item_occur / NO_OF_SEQUENCES
    return i

def generate_L(M, MIS, actual_support):
    l = []
    for item in M:
        if not (l) and (actual_support[item] >= MIS[item]):
            l.append(item)
        elif l and (actual_support[item] >= MIS[l[0]]):
            l.append(item)
    return l

def get_unique_items(sequences):
    unique_items = []
    for seq in sequences:
        for transact in seq:
            for item in transact:
                if item not in unique_items:
                    unique_items.append(item)
    return unique_items

def generate_F1(l,mis,actual_support):
    f1 = []
    for item in l:
        if actual_support[item] >= mis[item]:
            f1.append(item)
    return f1

I = get_unique_items(sequences)
M = sort_items(I, MIS)
ACTUAL_SUPPORT = item_actual_support(I,sequences)
L = generate_L(M, MIS, ACTUAL_SUPPORT)
F1 = generate_F1(L, MIS, ACTUAL_SUPPORT)
print(F1)