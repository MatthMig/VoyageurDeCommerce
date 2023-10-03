import copy
import queue


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
def regrets_calculation(matrix):
    max_regret = 0
    max_path = (0,0)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                continue
            regret = min(matrix[i][:j] + matrix[i][j+1:]) + min([matrix[k][j] for k in range(len(matrix)) if k != i])
            if regret > max_regret:
                max_regret = regret
                max_path = (i,j)
    return max_path[0], max_path[1], max_regret

def little_algo(c):
    tree = queue.PriorityQueue()
    reduction_matrix, h = reduction(c)
    i, j, max_regret = regrets_calculation(reduction_matrix)
    tree.put((h, Node(parent=None, lower_bound=h, matrix=reduction_matrix)))
    borne_sup = h
    best_leaf = None
    while not tree.empty():
        X = tree.get()[1]
        if X.lower_bound > borne_sup:
            continue
        R, h = reduction(X.matrix)
        i, j, max_regret = regrets_calculation(R)

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

        # Check if we have found a lower bound better than the current absolute superior bound
        if all(element == float('inf') for row in X.matrix for element in row) and lower_bound <= borne_sup:
            borne_sup = lower_bound
            best_leaf = X.son_R
    return best_leaf

def get_path(node):
    result = []
    while node is not None:
        if node.vertex is not None:
            result.append(node.vertex)
        node = node.parent
    return result[::-1]

matrix = [[float('inf'), 10, 15, 20],
          [10, float('inf'), 35, 25],
          [15, 35, float('inf'), 30],
          [20, 25, 30, float('inf')]]

print(get_path(little_algo(matrix)))