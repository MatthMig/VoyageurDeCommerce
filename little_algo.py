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
        starting_ending_cities = get_starting_ending_cities(get_path(X))
        i, j, max_regret = regrets_calculation(X.matrix, starting_ending_cities)

        # Single tour node near
        remaining_cities = cities_remaining(X.matrix)
        if remaining_cities <= 2:
            # If current path is not a possible tour, we do not consider it
            if len(get_path(X)) + remaining_cities < len(X.matrix):
                continue
            # Finish the tour if there is two cities remaining
            if remaining_cities == 2:
                R[i][j] = float('inf')
                X.son_R = Node(parent=X, lower_bound=X.lower_bound + h, matrix=R,
                           vertex=(i, j))
                X = X.son_R
                starting_ending_cities = get_starting_ending_cities(get_path(X))
                
            # Leaf node
            R = [[float('inf') for _ in range(len(R[i]))] for i in range(len(R))]
            X.son_R = Node(parent=X, lower_bound=X.lower_bound, matrix=R,
                           vertex=(starting_ending_cities[0][1], starting_ending_cities[0][0]))
            X = X.son_R

            # Check if we have found a lower bound better than the current absolute superior bound
            if X.lower_bound < sup_bound and X.vertex is not None:
                sup_bound = X.lower_bound
                best_leaf = X
            continue

        # Left branch (we do not take the path)
        R_ = copy.deepcopy(R)
        R_[i][j] = float('inf')
        lower_bound = X.lower_bound + max_regret
        tree.put((lower_bound, Node(parent=X, lower_bound=lower_bound, matrix=R_)))

        # Right branch (we do take the path)
        R[i] = [float('inf') for _ in range(len(R[i]))]
        for row in R:
            row[j] = float('inf')
        R[j][i] = float('inf')
        lower_bound = X.lower_bound + h
        tree.put((lower_bound, Node(parent=X, lower_bound=lower_bound, matrix=R, vertex = (i,j))))

    # Return the best path found
    result_path = get_path(best_leaf)
    # Check if solution is correct
    starting_ending_cities = get_starting_ending_cities(result_path)
    if starting_ending_cities[0][0] != starting_ending_cities[0][1]:
        print("RESULT NOT CORRECT, GRAPHIC IS CONNEX")
    return result_path

# Returns reduction of the matrix and sum of reducing constants
def reduction(matrix):
    matrix = copy.deepcopy(matrix)
    h = 0
    # Check if matrix has only infinite values
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
def regrets_calculation(matrix, starting_ending_cities=[]):
    matrix = copy.deepcopy(matrix)
    max_regret = -1
    max_path = (0,0)
    for st_ed in starting_ending_cities:
        matrix[st_ed[1]][st_ed[0]] = float('inf')
    matrix,h = reduction(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                continue
            regret = min(matrix[i][:j] + matrix[i][j+1:]) + min([matrix[k][j] for k in range(len(matrix)) if k != i])
            if regret > max_regret:
                max_regret = regret
                max_path = (i,j)
    return max_path[0], max_path[1], max_regret

# Get all starting and ending cities from a path, takes in account possible connexity of path
def get_starting_ending_cities(path):
    st_ed_all = []
    path_dict_from_to = {p[0]:p[1] for p in path}

    while path_dict_from_to:
        # Check all following travels
        st = From = list(path_dict_from_to.keys())[0]   # Get an initial travel
        while From in path_dict_from_to:
            To = path_dict_from_to.pop(From)
            From = To
        # Check all previous travels
        while st in [p[1] for p in path_dict_from_to.items()]:
            From = [p for p in path_dict_from_to.items() if p[1] == st][0]
            del path_dict_from_to[From[0]]
            st = From[0]
        st_ed_all.append((st, To))
    return st_ed_all

# Returns number of cities remaining in the matrix
def cities_remaining(matrix):
    cpt = 0
    for row in matrix:
        for i in row:
            if i != float('inf'):
                cpt += 1
                if cpt > 2:
                    return cpt
    return cpt

# Go from node to root and return list of all vertexes
def get_path(node):
    result = []
    while node is not None:
        if node.vertex is not None:
            result.append(node.vertex)
        node = node.parent
    return result[::-1]