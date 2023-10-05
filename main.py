import time

import benchmark
import brute_force
import little_algo

matrix = [  [float('inf'), 27, 43, 16, 30, 26],
            [7, float('inf'), 16, 1, 30, 25],
            [20, 13, float('inf'), 35, 5, 0],
            [21, 16, 25, float('inf'), 18, 18],
            [12, 46, 27, 48, float('inf'), 5],
            [23, 5, 5, 9, 5, float('inf')]]

start_time = time.time()
path_brute = brute_force.brute_force(matrix)
brute_execution_time = time.time() - start_time
print("Expected (brute force result): ", path_brute[0], "\ncost: ", path_brute[1],
        "\nExecution time: ", brute_execution_time, "s")

start_time = time.time()
path_little = little_algo.little_algo(matrix)
little_execution_time = time.time() - start_time
print("Little algo result: ", path_little, "\ncost: ", benchmark.get_cost(path_little, matrix),
        "\nExecution time: ", little_execution_time, "s")