# Python program to find
# maximal Bipartite matching.
import datetime
import csv

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
            # 0th based indexing
            matrix[int(key)-1][int(value)-1] = 1

    return matrix

if __name__ == '__main__':

    # First dataset
    dataset_pairs = parseData("../datasets/out.brunson_club-membership_club-membership.tsv")
    graph = parse_members(dataset_pairs)
    start = datetime.datetime.now()
    g = GFG(graph)
    end = datetime.datetime.now()
    print ("The maximum possible matching is %d " % g.maxBPM())

    print("time", end - start)

