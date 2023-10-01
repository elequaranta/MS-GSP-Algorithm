import copy
import time


def readInput(path):
    with open(path, 'r') as data:
        sequence = []
        for lines in data:
            transactions = lines[1:-2]
            parts = transactions.split("}{")
            lists = [part.strip("{}").split(",") for part in parts]
            seq = [[item.strip() for item in transact] for transact in lists]
            sequence.append(seq)
        data.close()
    return sequence


def load_MIS_sdc(path, items):
    read_MIS = dict()
    final_MIS = dict()
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if ('mis' in line.lower()):
                item = line[line.find("(") + 1:line.find(
                    ")")].strip()  # if we don't parse to integer it will be able to work with letters as items as well + with MIS(rest)
                value = float(line[line.find('=') + 1:].strip())
                read_MIS[item] = value
            elif ('sdc' in line.lower()):
                read_sdc = float(line[line.find('=') + 1:].strip())
    for item in items:
        if item in read_MIS.keys():
            final_MIS[item] = read_MIS[item]
        else:
            final_MIS[item] = read_MIS['rest']
    global MIS
    MIS = final_MIS
    global sdc
    sdc = read_sdc
    return final_MIS, read_sdc


def get_unique_items(sequences):
    items = []
    for sequence in sequences:
        for transaction in sequence:
            for element in transaction:
                if element not in items:
                    items.append(element)
    return items


def init_pass(M, sequences):
    # scan the sequences once to count the support of each item
    sup_counts = dict.fromkeys(M, 0)
    unique = get_unique_items(sequences)
    for sequence in sequences:
        for item in unique:
            if any(item in transaction for transaction in sequence):
                previous = sup_counts[item]
                sup_counts[item] = previous + 1
    # find first item in M meeting its minsup requirement:
    found = False
    L = []
    for i in range(0, len(M)):
        while found == False:
            item = M[i]
            if sup_counts[item] >= MIS[item] * len(sequences):
                L.append(item)
                found = True
                first_idx = i
    # find every subsequent item satisfying the first item's minsup
    if found == True:
        for j in range(first_idx + 1, len(M)):
            item = M[j]
            if sup_counts[item] >= MIS[M[first_idx]] * len(sequences):
                L.append(item)
    return L, sup_counts


def get_itemset_ms(seq):
    # find the minimum support of an itemset (= lowest minimum support of the items)
    # and return the position of the element in the transaction (as an index)
    minsups = []
    for transaction in seq:
        for item in transaction:
            minsups.append(MIS[item])  # this is an ordered list of the minsups of each item in the transaction
    min_value = min(minsups)
    min_position = [i for i, x in enumerate(minsups) if x == min_value]
    return min_value, min_position


def generate_f1(l, sup_counts, sequences):
    f1 = []
    for item in l:
        if sup_counts[item] >= MIS[item] * len(sequences):
            f1.append([item])
    return f1


def level2_candidate_gen(num_seq, L, sup_counts):
    item_sups = {k: val / num_seq for k, val in sup_counts.items()}
    candidates = []
    for l in L:
        if item_sups[l] >= MIS[l]:
            candidates.extend([[[l],[l]],[[l,l]]])
            for h in L[L.index(l) + 1:]:
                if (item_sups[h] >= MIS[l]) and (abs(item_sups[h] - item_sups[l]) <= sdc):
                    candidates.extend([[[l, h]], [[l], [h]], [[h], [l]]])
    return candidates


def candidate_gen(F_previous):
    C = []
    for s1 in F_previous:
        for s2 in F_previous:
            if(s1==[['9', '1']] and s2==[['9'], ['1']]):
                print('here')
            minsup1, index1 = get_itemset_ms(s1)
            minsup2, index2 = get_itemset_ms(s2)
            # if first item in s1 or last item in s2 is the only one with minimum support:
            if (index1 == [0]):
                flag1 = (delete_element(s1, 1) == delete_element(s2, get_length(s2) - 1))
                flag2 = (MIS[last_item(s2)] >= MIS[first_item(s1)])
                if ((delete_element(s1, 1) == delete_element(s2, get_length(s2) - 1)) & (MIS[last_item(s2)] >= MIS[first_item(s1)])):
                    if (get_size(s2[-1]) == 1):
                        c = copy.deepcopy(s1)
                        c.append([last_item(s2)])

                        if(c==['9', '1', '1']):
                            print('here')
                        if(check_sdc(c) & (c not in C)):
                            C.append(c)
                        if ((get_length(s1) == 2 & get_length(s2) == 2) & (MIS[last_item(s2)] >= MIS[last_item(s1)])):
                            c = copy.deepcopy(s1)
                            last_c = copy.deepcopy([c[-1]])
                            last_c.append([last_item(s2)])
                            del c[-1]
                            c.extend(last_c)

                            if(c==['9', '1', '1']):
                                print('here')
                            if(check_sdc(c) & (c not in C)):
                                C.append(c)
                    elif(((get_length(s1) == 2 & get_size(s1) == 1) & (MIS[last_item(s2)] >= MIS[last_item(s1)])) or (get_length(s1) > 2)):
                        c = copy.deepcopy(s1)
                        last_c = copy.deepcopy(c[-1])
                        last_c.append(last_item(s2))
                        del c[-1]
                        c.append(last_c)
                        if(c==['9', '1', '1']):
                            print('here')

                        if(check_sdc(c) & (c not in C)):
                            C.append(c)
            elif (index2 == [get_length(s2) - 1]):
                if ((delete_element(s2, get_length(s2) - 2) == delete_element(s1, 0)) & (MIS[first_item(s1)] >= MIS[last_item(s2)])):
                    if (get_size(s1[0]) == 1):
                        c = copy.deepcopy(s2)
                        c[0].append(first_item(s1))

                        if(c==['9', '1', '1']):
                            print('here')
                        if(check_sdc(c) & (c not in C)):
                            C.append(c)
                        if ((get_length(s2) == 2 & get_length(s2) == 2) & (MIS[first_item(s1)] >= MIS[first_item(s2)])):
                            c = [[first_item(s1)]]
                            c[0].append(first_item(s2))
                            c.extend(s2[1:])

                            if(c==['9', '1', '1']):
                                print('here')
                            if(check_sdc(c) & (c not in C)):
                                C.append(c)
                    elif(((get_length(s2) == 2 & get_size(s2) == 1) & (MIS[first_item(s1)] >= MIS[first_item(s2)])) or (get_length(s2) > 2)):
                        c = [[first_item(s1)]]
                        c[0].append(first_item(s2))
                        c.extend(s2[1:])

                        if(c==['9', '1', '1']):
                            print('here')
                        if(check_sdc(c) & (c not in C)):
                            C.append(c)
            # general case (= neither the first item in s1 nor the last item in s2 is the only one with minimum support)
            else:
                # s1 joins with s2 if s1-{first} == s2-{last}
                if (delete_element(s1, 0) == delete_element(s2, get_length(s2) - 1)):
                    if get_size(s2[-1]) == 1:
                        c = copy.deepcopy(s1)
                        c.append([last_item(s2)])

                        if(check_sdc(c) & (c not in C)):
                            C.append(c)
                    else:
                        c = copy.deepcopy(s1)
                        last_c = copy.deepcopy(c[-1])
                        last_c.append(last_item(s2))
                        del c[-1]
                        c.append(last_c)

                        if(check_sdc(c) & (c not in C)):
                            C.append(c)
        
        pruned_C = prune_candidates(C, F_previous)

    return pruned_C


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
        break
    return first


def last_item(sequence):
    for t in sequence:
        last = t[-1]
    return last

def lexicographic_order(candidate):
    sorted_c = []
    for t in candidate:
        sorted_t = sorted(t)
        sorted_c.append(sorted_t)
    return sorted_c
        

def delete_element(passed_sequence, idx):
    sequence = copy.deepcopy(passed_sequence)
    if (idx >= 0 & idx < get_length(sequence)):
        initial_tracker = 0
        final_tracker = 0
        for transaction in sequence:
            initial_tracker = final_tracker
            num_elements = len(transaction)
            final_tracker = initial_tracker + num_elements
            if (final_tracker > idx):  # the element to delete is in this sequence
                del transaction[idx - initial_tracker]
                break
        new_sequence = [transaction for transaction in sequence if get_length(transaction) > 0]
        return new_sequence
    else:
        return []


def prune_candidates(C, F):
    C_final = []
    for c in C:
        if(c == ['9', '1', '1']):
            print('here')
        ms, idx = get_itemset_ms(c)
        tested = 0
        matches = 0
        for i in range(0, get_length(c)):
            if not (idx == [i]):
                tested = tested + 1
                c_short = delete_element(c, i)
                for f in F:
                    if (subsequence(c_short, f)):
                        matches = matches + 1
                        break
        if (matches == tested):
            C_final.append(c)
    return C_final


def subsequence(sub, super):
    last_idx = -1
    matches = 0
    for e in sub:
        for i in range(0, get_size(super)):
            if(contains_transaction(e, super[i]) & (i > last_idx)):
                last_idx = i
                matches = matches + 1
                break
    if (matches == get_size(sub)):
        return True
    else:
        return False
    
def contains_transaction(t, T):
    temp = copy.deepcopy(T)
    try:
        for el in t:
            temp.remove(el)
        return True
    except ValueError:
        return False
    
def check_sdc(candidate):
    unique = [element for transaction in candidate for element in transaction]
    mis_list = []
    for el in unique:
        mis_list.append(MIS[el])
    max_val = max(mis_list)
    min_val = min(mis_list)
    if((max_val - min_val) <= sdc):
        return True
    else:
        return False
    
#def remove_duplicate_sequences(Fk):


# S = [['10'], ['20', '40'], ['30', '70'], ['10', '30', '80', '20']]
# s = [['10'], ['30'], ['20', '80']]
# subsequence(s, S)

def MSGSP(seq_path, MIS_path):
    sequences = readInput(seq_path)
    num_sequences = len(sequences)
    items = get_unique_items(sequences)
    load_MIS_sdc(MIS_path, items)
    M = list(dict(sorted(MIS.items(), key=lambda x: x[1])).keys())
    L, support_counts = init_pass(M, sequences)
    F_prev = generate_f1(L, support_counts, sequences)
    k = 1
    F = F_prev
    while (get_length(F_prev) != 0):
        k = k + 1
        Fk = []
        if (k == 2):
            C = level2_candidate_gen(num_sequences, L, support_counts)
        else:
            C = candidate_gen(F_prev)
        for c in C:
            counter = 0
            minMS, minIdx = get_itemset_ms(c)
            for sequence in sequences:
                if (subsequence(c, sequence)):
                    counter = counter + 1
            if (counter >= minMS * num_sequences):
                Fk.append(c)
        F.extend(Fk)
        F_prev = copy.deepcopy(Fk)
    return F


def main():
    seq_path = '/Users/elequaranta/Documents/Chicago/CS583/MS-GSP/00/data.txt'
    param_path = '/Users/elequaranta/Documents/Chicago/CS583/MS-GSP/00/params.txt'
    start = time.time()
    frequent = MSGSP(seq_path, param_path)
    end = time.time()
    print(frequent)
    print('Time elapsed: ', end-start)
    file = open('/Users/elequaranta/Documents/Chicago/CS583/MS-GSP/00/results.txt', 'w')
    for seq in frequent:
        file.write(str(seq) + "\n")
    file.close()


#  Ctest = [[['40'], ['50'], ['40'], ['30']]]
#  Ftest = [[['40'], ['50'], ['30']], [['40'], ['50'], ['40']], [['50'], ['40'], ['30']], [['40'], ['40'], ['30']]]

#  prune_candidates(Ctest, Ftest)

if __name__ == '__main__':
    main()
