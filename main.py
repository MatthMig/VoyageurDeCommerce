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
    i,j,regret = regrets_calculation(reduction_matrix)
    root = Node(parent=None, lower_bound=h, matrix=reduction_matrix)
    tree.put((h, root))
    absolute_lower_bound = h
    while not tree.empty():
        X = tree.get()[1]
        R, h = reduction(X.matrix)
        if h == float('inf'):
            continue
        i, j, regret = regrets_calculation(R)

        # Left branch (we do not take the path)
        R_ = copy.deepcopy(R)
        R_[i][j] = float('inf')
        lower_bound = X.lower_bound + regret
        if lower_bound <= absolute_lower_bound:
            absolute_lower_bound = lower_bound
        tree.put((lower_bound, Node(parent=X, lower_bound=lower_bound, matrix=R_)))

        # Right branch (we do take the path)
        R[i] = [float('inf') for _ in range(len(R[i]))]
        for row in R:
            row[j] = float('inf')
        R[j][i] = float('inf')
        #lower_bound = X.lower_bound + h
        lower_bound = float('inf')
        if lower_bound <= absolute_lower_bound:
            absolute_lower_bound = lower_bound
        tree.put((lower_bound, Node(parent=X, lower_bound=lower_bound, matrix=R, vertex = (i,j))))
    return root

matrix = [[float('inf'), 10, 15, 20],
          [10, float('inf'), 35, 25],
          [15, 35, float('inf'), 30],
          [20, 25, 30, float('inf')]]

root = little_algo(matrix)

def find_min_leaf_with_parents(root):
    min_leaf = None
    parent_stack = []

    def dfs(node):
        nonlocal min_leaf
        if not node:
            return

        parent_stack.append(node.vertex)

        if not node.son_L and not node.son_R:
            if min_leaf is None or node.lower_bound < min_leaf.lower_bound:
                min_leaf = node
        else:
            if not node.son_L or (node.son_R and node.son_R.lower_bound < node.son_L.lower_bound):
                dfs(node.son_R)
            else:
                dfs(node.son_L)

        parent_stack.pop()

    dfs(root)
    
    return parent_stack

print(find_min_leaf_with_parents(root))