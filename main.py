import random

import brute_force
import little_algo

matrix = [[float('inf'), 10, 15, 20],
          [10, float('inf'), 35, 25],
          [15, 35, float('inf'), 30],
          [20, 25, 30, float('inf')]]

"""matrix = [  [float('inf'), 27, 43, 16, 30, 26],
            [7, float('inf'), 16, 1, 30, 25],
            [20, 13, float('inf'), 35, 5, 0],
            [21, 16, 25, float('inf'), 18, 18],
            [12, 46, 27, 48, float('inf'), 5],
            [23, 5, 5, 9, 5, float('inf')]]"""

def get_cost(path, matrix):
    cost = 0
    for p in path:
        cost += matrix[p[0]][p[1]]
    return cost

# Generate random matrix to test the algorithm
def random_matrix_generator(n):
    matrix = [[None for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = float('inf')
            elif j < i:
                matrix[i][j] = matrix[j][i]
            else:
                matrix[i][j] = random.randint(1, 50)
    return matrix

for i in range(3,10):
    matrix = random_matrix_generator(i)
    path_brute = brute_force.brute_force(matrix)
    print("\nExpected (brute force result): ", path_brute[0], "\ncost: ", path_brute[1])
    path_little = little_algo.little_algo(matrix)
    print("Little algo result: ", path_little, "\ncost: ", get_cost(path_little, matrix))