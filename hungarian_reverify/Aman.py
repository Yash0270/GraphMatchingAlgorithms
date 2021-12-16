from scipy.optimize import linear_sum_assignment
import numpy as np
import time
import csv


from hungarian_algorithm import algorithm

def parseData(filename):
    pairs = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            left = row[0]
            right = row[1]

            if left == right:
                continue

            if right in pairs.keys():
                if left in pairs[right].keys():
                    continue

            if left in pairs.keys():
                pairs[left][right] = 1
            else:
                pairs[left] = {}
                pairs[left][right] = 1
    print(pairs)
    return pairs


def parse_members(pairs):
    n = 100
    matrix = [[0 for i in range(n+1)] \
              for j in range(n+1)]

    for key in pairs:
        for value in pairs[key]:
            print( str(key) + " " + str(value))
            matrix[int(key)][int(value)] = 1

    return matrix

def compute_maximum_matching(A):
    start = time.time()
    A = np.array(A)
    row_ind, col_ind = linear_sum_assignment(A, maximize=True)
    end = time.time()
    print("Run Time: ", end - start, "seconds")
    return A[row_ind, col_ind].sum()

if __name__ == '__main__':
    member2group = parseData("out.brunson_club-membership_club-membership.tsv")
    output = algorithm.find_matching(member2group, matching_type='max', return_type='list')
    print("tem")
    # members_matrix = parse_members(member2group)
    # print("maximum matchig : " +  compute_maximum_matching(members_matrix))
