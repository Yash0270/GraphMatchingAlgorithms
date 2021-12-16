import numpy as np
from km_matcher import KMMatcher
from scipy.optimize import linear_sum_assignment
import numpy as np
import time
import csv

def parseData(filename):
    pairs = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            left = row[0]
            right = row[1]
            pairs.setdefault(left, set()).add(right)
    return pairs


def parse_members(pairs):
    n = len(pairs.keys())
    matrix = [[0 for i in range(n+1)] \
              for j in range(n+1)]

    for key in pairs:
        for value in pairs[key]:
            print( str(key) + " " + str(value))
            matrix[int(key)][int(value)] = 1

    return matrix



if __name__ == '__main__':
    member2group = parseData("out.brunson_club-membership_club-membership.tsv")
    weights = parse_members(member2group)
    st = time.time()
    matcher = KMMatcher(weights)
    best = matcher.solve(verbose=True)
    ed = time.time()

    print('time consuming of size ({}, {}) is {:.4f} seconds'.format(len(member2group), len(member2group), ed - st))