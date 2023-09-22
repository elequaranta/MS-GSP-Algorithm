import re



def readInput():
    with open('/Users/elequaranta/Documents/Chicago/CS583/MS-GSP/data.txt', 'r') as data:
        sequence = []
        for lines in data:
            transactions = lines[1:-2]
            parts = transactions.split("}{")
            lists = [part.strip("{}").split(",") for part in parts]
            seq = [[item.strip() for item in transact] for transact in lists]
            sequence.append(seq)
        data.close()
    global sequences
    sequences = sequence

def load_MIS_sdc(path, items):
    read_MIS = dict()
    final_MIS = dict()
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if('mis' in line.lower()):
                item = line[line.find("(")+1:line.find(")")].strip() #if we don't parse to integer it will be able to work with letters as items as well + with MIS(rest)
                value = float(line[line.find('=')+1:].strip())
                read_MIS[item] = value
            elif('sdc' in line.lower()):
                read_sdc = float(line[line.find('=')+1:].strip())
    for item in items:
        if item in read_MIS.keys():
            final_MIS[item] = read_MIS[item]
        else:
            final_MIS[item] = read_MIS['rest']
    global MIS 
    MIS = final_MIS
    global sdc
    sdc =  read_sdc         


def get_unique_items(sequences):
    items = []
    for sequence in sequences:
        for transaction in sequence:
            for element in transaction:
                if element not in items:
                    items.append(element) 
    return items

def init_pass():
    M = list(dict(sorted(MIS.items(), key=lambda x:x[1])).keys())
    #scan the sequences once to count the support of each item
    sup_counts = dict.fromkeys(M, 0)
    unique = get_unique_items(sequences)
    for sequence in sequences:
        for item in unique:
            if any(item in transaction for transaction in sequence):
                previous = sup_counts[item]
                sup_counts[item] = previous + 1
    #find first item in M meeting its minsup requirement:
    found = False
    L = []
    for i in range (0, len(M)):
        while found == False:
            item = M[i]
            if sup_counts[item] >= MIS[item]*len(sequences):
                L.append(item)
                found = True
                first_idx = i
    #find every subsequent item satisfying the first item's minsup
    if found == True:
        for j in range (first_idx+1, len(M)):
            item = M[j]
            if sup_counts[item] >= MIS[M[first_idx]]*len(sequences):
                L.append(item)
    return L, sup_counts

def get_itemset_ms(sequence):
    #find the minimum support of an itemset (= lowest minimum support of the items)
    #and return the position of the element in the transaction (as an index)
    minsups = []
    for transaction in sequence:
        for item in transaction:
            minsups.append(MIS[item]) #this is an ordered list of the minsups of each item in the transaction
    min_value = min(minsups)
    min_position = [i for i, x in enumerate(minsups) if x == min_value]
    return min_value, min_position


def generate_f1(l,sup_counts):
    f1 = []
    for item in l[1:]:
        if sup_counts[item] >= MIS[item]*len(sequences):
            f1.append(item)
    return f1

def level2_candidate_gen(L,sup_counts):
    item_sups= {k : val/len(sequences) for k, val in sup_counts.items()}
    #item_sups = sup_counts / len(sequences)
    candidates = []
    for l in L:
        if item_sups[l] >= MIS[l]:
            for h in L[L.index(l)+1:]:
                if (item_sups[h] >= MIS[l]) and (abs(item_sups[h] - item_sups[l]) <= sdc) :
                    candidates.extend([[[l,h]],[[l],[h]],[[h],[l]]])
    return candidates




def get_size(sequence):
    return len(sequence)


def get_length(sequence):
    length = 0
    for t in sequence:
        length = length + len(t)
    return length

def first_item(sequence):
    for t in sequence:
        first = t[0]
        pass
    return first

def last_item(sequence):
    for t in sequence:
        last = t[-1]
    return last

def main():
    readInput()   
    items = get_unique_items(sequences)
    print(items)
    load_MIS_sdc('/Users/elequaranta/Documents/Chicago/CS583/MS-GSP/params.txt', items)
    print(MIS) 
    print(sdc)  
    L, sup_counts = init_pass()
    print(L)
    print(sup_counts)
    F1 = generate_f1(L, sup_counts)
    print(F1)
    c2 = level2_candidate_gen(L, sup_counts)
    print(c2)

    print(get_itemset_ms(c2[0]))

if __name__ == '__main__':
    main()