# Python program to find
# maximal Bipartite matching.
import datetime
import csv
import pickle
from collections import defaultdict
import pandas as pd

class GFG:
    def __init__(self, graph):

        # residual graph
        self.graph = graph
        self.ppl = len(graph)
        self.jobs = len(graph[0])

    # A DFS based recursive function
    # that returns true if a matching
    # for vertex u is possible
    def bpm(self, u, matchR, seen):

        # Try every job one by one
        for v in range(self.jobs):

            # If applicant u is interested
            # in job v and v is not seen
            if self.graph[u][v] and seen[v] == False:

                # Mark v as visited
                seen[v] = True

                '''If job 'v' is not assigned to
                an applicant OR previously assigned
                applicant for job v (which is matchR[v])
                has an alternate job available.
                Since v is marked as visited in the
                above line, matchR[v] in the following
                recursive call will not get job 'v' again'''
                if matchR[v] == -1 or self.bpm(matchR[v],
                                               matchR, seen):
                    matchR[v] = u
                    return True
        return False

    # Returns maximum number of matching
    def maxBPM(self):
        '''An array to keep track of the
        applicants assigned to jobs.
        The value of matchR[i] is the
        applicant number assigned to job i,
        the value -1 indicates nobody is assigned.'''
        matchR = [-1] * self.jobs

        # Count of jobs assigned to applicants
        result = 0
        for i in range(self.ppl):

            # Mark all jobs as not seen for next applicant.
            seen = [False] * self.jobs

            # Find if the applicant 'u' can get a job
            if self.bpm(i, matchR, seen):
                result += 1
        return result


def parseData(filename, delimiter):
    pairs = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            left = row[0]
            right = row[1]
            pairs.setdefault(left, set()).add(right)
    return pairs

def parse_data_csv(filename):
    pairs = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            left = row[0]
            right = row[1]
            pairs.setdefault(left,set()).add(right)
    return pairs

def parse_members(pairs):
    n = len(pairs.keys())
    matrix = [[0 for i in range(n+1)] \
              for j in range(n+1)]

    for key in pairs:
        for value in pairs[key]:
            print( str(key) + " " + str(value))
            # 0th based indexing
            matrix[int(key)-1][int(value)-1] = 1

    return matrix

def get_membership_dataset_graph():
    dataset_pairs = parseData("../datasets/out.brunson_club-membership_club-membership.tsv", ' ')
    return parse_members(dataset_pairs)


def get_fifa_dataset_graph():
    rows = []
    file = open("../datasets/fifa_players.csv")
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
    rows = rows[1:]
    country_idx_map, i = {}, 0
    for source, dest, _ in rows:
        if source not in country_idx_map:
            country_idx_map[source] = i
            i += 1
        if dest not in country_idx_map:
            country_idx_map[dest] = i
            i += 1
    num_countries = len(country_idx_map)
    matrix = [[0 for i in range(num_countries)] \
              for j in range(num_countries)]

    for source, dest, _ in rows:
        matrix[country_idx_map[source]][country_idx_map[dest]] = 1

    return matrix


def get_yelp_dataset_graph():
    file_path = '../datasets/yelp_dataset_8000_users.pkl'
    infile = open(file_path, 'rb')
    df = pickle.load(infile)
    G = defaultdict(dict)
    infile.close()

    user_id_map, review_id_map = {}, {}
    unique_user_ids, unique_review_ids = df.user_id.unique(), df.review_id.unique()
    for i, user_id in enumerate(unique_user_ids):
        user_id_map[user_id] = i
    for i, review_id in enumerate(unique_review_ids):
        review_id_map[review_id] = i

    for user_id, review_id in zip(df['user_id'], df['review_id']):
        G[user_id][review_id] = 1

    matrix = [[0 for j in range(len(unique_review_ids))] for i in range(len(unique_user_ids))]

    for user_id in G:
        for review_id in G[user_id].keys():
            matrix[user_id_map[user_id]][review_id_map[review_id]] = 1

    return matrix


def get_members_dataset_graph():
    rows = []
    file = open('../datasets/member-to-group-edges.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        rows.append(row)
    rows = rows[1:]
    idx_map, i = {}, 0
    for source, dest, _ in rows:
        if source not in idx_map:
            idx_map[source] = i
            i += 1
        if dest not in idx_map:
            idx_map[dest] = i
            i += 1
    n = len(idx_map)
    matrix = [[0 for i in range(n)] \
              for j in range(n)]

    for source, dest, _ in rows:
        matrix[idx_map[source]][idx_map[dest]] = 1

    return matrix


if __name__ == '__main__':

    # graph = get_membership_dataset_graph()
    # graph = get_fifa_dataset_graph()
    # graph = get_yelp_dataset_graph()
    graph = get_members_dataset_graph()

    start = datetime.datetime.now()
    g = GFG(graph)
    end = datetime.datetime.now()
    print ("The maximum possible matching is %d " % g.maxBPM())

    print("time", end - start)

