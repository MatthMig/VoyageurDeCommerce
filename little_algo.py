import copy
import queue

import brute_force


class Node:
    def __init__(self, parent, lower_bound, matrix, vertex=None):
        self.parent = parent
        self.vertex = vertex
        self.lower_bound = lower_bound
        self.matrix = matrix
        self.son_L = None
        self.son_R = None

        if self.parent is not None:
            if self.vertex is None:
                self.parent.son_L = self
            else:
                self.parent.son_R = self

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.lower_bound == other.lower_bound
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.lower_bound < other.lower_bound
        raise TypeError("Comparison with unsupported type")

    def __le__(self, other):
        if isinstance(other, Node):
            return self.lower_bound <= other.lower_bound
        raise TypeError("Comparison with unsupported type")

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.lower_bound > other.lower_bound
        raise TypeError("Comparison with unsupported type")

    def __ge__(self, other):
        if isinstance(other, Node):
            return self.lower_bound >= other.lower_bound
        raise TypeError("Comparison with unsupported type")

# Implementation of the algorithm
def little_algo(c):
    if len(c) <= 2:
        print("The matrix is too small to be solved with this algorithm")
        return None

    # Tree initilisation
    tree = queue.PriorityQueue()
    reduction_matrix, h = reduction(c)
    i, j, max_regret = regrets_calculation(reduction_matrix)
    tree.put((h, Node(parent=None, lower_bound=h, matrix=reduction_matrix)))

    # Bound init
    sup_bound = float('inf')
    best_leaf = None

    # Exploration
    while not tree.empty():
        X = tree.get()[1]

        # Bound
        if X.lower_bound > sup_bound:
            continue

        R, h = reduction(X.matrix)
        starting_ending_city = get_starting_ending_city(get_path(X))
        i, j, max_regret = regrets_calculation(R, starting_ending_city)

        # Single tour node near
        if single_tour_node_near(X.matrix):
            #print(get_path(X))
            # If current path is not a possible tour, we do not consider it
            if len(get_path(X)) < len(X.matrix) - 1:
                continue
            # Check where go to finish the tour
            j,i = starting_ending_city
            # Leaf node
            R[i] = [float('inf') for _ in range(len(R[i]))]
            R[j][i] = float('inf')
            X.son_R = Node(parent=X, lower_bound=X.lower_bound + h, matrix=R, vertex = (i,j))
            X = X.son_R

            # Check if we have found a lower bound better than the current absolute superior bound
            if lower_bound < sup_bound and X.vertex is not None:
                sup_bound = lower_bound
                best_leaf = X
            continue

        # Left branch (we do not take the path)
        R_ = copy.deepcopy(R)
        R_[i][j] = float('inf')
        lower_bound = X.lower_bound
        tree.put((lower_bound, Node(parent=X, lower_bound=lower_bound, matrix=R_)))

        # Right branch (we do take the path)
        R[i] = [float('inf') for _ in range(len(R[i]))]
        for row in R:
            row[j] = float('inf')
        R[j][i] = float('inf')
        lower_bound = X.lower_bound + h
        tree.put((lower_bound, Node(parent=X, lower_bound=lower_bound, matrix=R, vertex = (i,j))))

    return get_path(best_leaf)

# Returns reduction of the matrix and sum of reducing constants
def reduction(matrix):
    matrix = copy.deepcopy(matrix)
    h = 0
    if [i for row in matrix for i in row if i != float('inf')] == []:
        return matrix, float('inf')
    for i,r in enumerate(matrix):
        if r.count(float('inf')) == len(r):
            continue
        h += min(r)
        matrix[i] = [j-min(r) for j in r]
    for i in range(len(matrix[0])):
        column = [matrix[j][i] for j in range(len(matrix))]
        if column.count(float('inf')) == len(column):
            continue
        h += min(column)
        for j in range(len(matrix)):
            matrix[j][i] -= min(column)
    return matrix, h

# Returns max regret and matrix position corresponding to it
def regrets_calculation(matrix, starting_ending_city=[]):
    matrix = copy.deepcopy(matrix)
    max_regret = -1
    max_path = (0,0)
    if starting_ending_city:
        matrix[starting_ending_city[1]][starting_ending_city[0]] = float('inf')
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                continue
            regret = min(matrix[i][:j] + matrix[i][j+1:]) + min([matrix[k][j] for k in range(len(matrix)) if k != i])
            if regret > max_regret:
                max_regret = regret
                max_path = (i,j)
    return max_path[0], max_path[1], max_regret

def get_starting_ending_city(path):
    st_ed = [None, None]
    from_cities = [p[0] for p in path]
    to_cities = [p[1] for p in path]
    for s in from_cities:
        if not s in to_cities:
            st_ed[0] = s
    for p in to_cities:
        if not p in from_cities:
            st_ed[1] = p
            return st_ed

def single_tour_node_near(matrix):
    cpt = 0
    for row in matrix:
        for i in row:
            if i != float('inf'):
                cpt += 1
                if cpt > 2:
                    return False
    return True

# Go from node to root and return list of all vertexes
def get_path(node):
    result = []
    while node is not None:
        if node.vertex is not None:
            result.append(node.vertex)
        node = node.parent
    return result[::-1]