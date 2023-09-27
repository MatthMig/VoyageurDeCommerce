import copy
import queue


class Node:
    def __init__(self, parent, lower_bound, reduction_matrix, vertex=None, son_L=None, son_R=None):
        self.parent = parent
        self.vertex = vertex
        self.lower_bound = lower_bound
        self.reduction_matrix = reduction_matrix
        self.son_L = son_L
        self.son_R = son_R

    def get_tour(self):
        tour = [self.vertex]
        node = self
        while node.parent is not None:
            node = node.parent
            if node.vertex is not None:
                tour.append(node.vertex)
        return tour[::-1]
    
def reduction(matrix):
    h = 0
    for i,r in enumerate(matrix):
        h += min(r)
        matrix[i] = [j-min(r) for j in r]
    for i in range(len(matrix[0])):
        column = [matrix[j][i] for j in range(len(matrix))]
        h += min(column)
        for j in range(len(matrix)):
            matrix[j][i] -= min(column)
    return matrix, h

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
    reduction_matrix, h = reduction(copy.deepcopy(c))
    i,j,regret = regrets_calculation(reduction_matrix)
    tree.put((h, Node(parent=None, lower_bound=h, reduction_matrix=reduction_matrix)))
    z0 = float('inf')
    best_ending_node_tour = None
    X = tree.get()[1]

    while True:
        k,l,regret = regrets_calculation(X.reduction_matrix)

        # Left branch
        X.son_L = Node(parent=X, lower_bound=X.lower_bound + regret, reduction_matrix=X.reduction_matrix)
        Y_ = X.son_L
        tree.put((Y_.lower_bound, Y_))

        # Right branch
        reduction_matrix.pop(k)
        for row in reduction_matrix:
            row.pop(l)
        
        m,p = X.get_path((k,l))
        # Avoid subtours
        # Get Starting point
        node = X
        while node.parent is not None:
            node = node.parent
            if node.vertex is not None:
                p = node.vertex[0]
        # Get Ending point
        node = X
        while node.son_R is not None:
            node = node.son_R
            if node.vertex is not None:
                m = node.vertex[1]
        reduction_matrix[m][p] = float('inf')

        reduction_matrix, h = reduction(reduction_matrix)
        i,j,regret = regrets_calculation(reduction_matrix)
        X.son_R = Node(parent=X, lower_bound=X.lower_bound + h, reduction_matrix=reduction_matrix, vertex=(k,l))
        Y = X.son_R
        tree.put((Y.lower_bound, Y))

        # Check if single tour node is near to complete it and update z0 and current ending node of best tour
        if len(reduction_matrix) == len(reduction_matrix[0]) == 2:
            if Y.lower_bound < z0:
                z0 = Y.lower_bound
                best_ending_node_tour = Y
        
        X = tree.get()[1]
        if node.lower_bound <= z0:
            return best_ending_node_tour.get_tour()
        if X == Y:
            continue
        cost_matrix = copy.deepcopy(c)
        for i,vertex in enumerate(X.get_tour()):
            cost_matrix[vertex[0]-i][vertex[1]-i] = 0


matrix = [  [float('inf'), 27, 43, 16, 30, 26],
            [7, float('inf'), 16, 1, 30, 25],
            [20, 13, float('inf'), 35, 5, 0],
            [21, 16, 25, float('inf'), 18, 18],
            [12, 46, 27, 48, float('inf'), 5],
            [23, 5, 5, 9, 5, float('inf')]]

little_algo(matrix)
