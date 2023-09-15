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



def generate_f1(sequences,MIS):
    f1_mis = {}
    no_of_seq = len(sequences)
    print(no_of_seq)
    F1 = {}
    for seq in sequences:
        for transact in seq:
            for item in transact:
                if item not in f1_mis.keys():
                    f1_mis[item] = MIS.get(item, MIS['rest'])
    f1_mis = dict(sorted(f1_mis.items(), key=lambda item: item[1]))
    for f1_item in f1_mis:
        item_occur = 0
        for seq in sequences:
            for transact in seq:
                if f1_item in transact:
                    item_occur+=1
                    break
        F1[f1_item] = item_occur/no_of_seq
    
    for k,v in f1_mis.items():  
        if v > F1[k]:
            del F1[k]
    print(F1)
    print(f1_mis)
generate_f1(sequences,MIS)