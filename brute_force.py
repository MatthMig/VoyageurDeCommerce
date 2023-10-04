import copy


def brute_force(matrix, path=[], cost=0, origin=None):
    best_cost = cost
    best_path = path
    if origin is None:
        origin = [i for i in range(len(matrix))]
    for i in origin:
        for j in range(len(matrix[i])):
            if matrix[i][j] == float('inf'):
                continue
            # To avoid subtours
            if path and j == path[0][0] and len(path) < len(matrix)-1:
                continue
            new_matrix = copy.deepcopy(matrix)
            new_matrix[i] = [float('inf') for _ in range(len(new_matrix[i]))]
            new_matrix[j][i] = float('inf')
            for row in new_matrix:
                row[j] = float('inf')
            son_path, son_cost = brute_force(new_matrix, path + [(i,j)], cost + matrix[i][j], origin=[j])
            if best_cost == cost or son_cost < best_cost:
                best_cost = son_cost
                best_path = son_path
    return best_path, best_cost