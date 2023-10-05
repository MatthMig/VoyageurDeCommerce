import random
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import brute_force
import little_algo


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
            else:
                matrix[i][j] = random.randint(1, 100)
    return matrix

df = pd.DataFrame([], columns=["Size", "Time_Algorithm_Little", "Time_Algorithm_Brute", "Cost_error"])

for i in range(3,8): # sizes of the matrix
    for _ in range(100): # number of tests for each size
        matrix = random_matrix_generator(i)
        print("\nMatrix of size ", i, "x", i)

        start_time = time.time()
        path_brute = brute_force.brute_force(matrix)
        brute_execution_time = time.time() - start_time
        cost_brute = path_brute[1]
        print("Expected (brute force result): ", path_brute[0], "\ncost: ", cost_brute,
            "\nExecution time: ", brute_execution_time, "s")

        start_time = time.time()
        path_little = little_algo.little_algo(matrix)
        little_execution_time = time.time() - start_time
        cost_little = get_cost(path_little, matrix)
        print("Little algo result: ", path_little, "\ncost: ", cost_little,
            "\nExecution time: ", little_execution_time, "s")
        
        row = [i, little_execution_time, brute_execution_time, abs(cost_brute - cost_little)/cost_brute*100]
        df.loc[len(df)] = row

# Plot results
df_mean = df.groupby(['Size']).agg({
                'Time_Algorithm_Little': 'mean',
                'Time_Algorithm_Brute': 'mean',
                'Cost_error': 'mean'
            }).reset_index()

sns.lineplot(data=df_mean, x="Size", y="Cost_error", color="red", label="Cost error")
plt.ylabel('Mean  relative cost error of the algorithm (%)')
plt.ylim(0, 100)
plt.legend(loc='upper left', title="Cost error")
ax2 = plt.twinx()
ax2.set_ylabel('Execution time of algorithm (s)')
df_mean_timeplot = pd.melt(df_mean[["Size", "Time_Algorithm_Little", "Time_Algorithm_Brute"]], id_vars=['Size'], var_name='Algorithm', value_name='Execution Time')
sns.lineplot(data=df_mean_timeplot, x="Size", y="Execution Time", hue="Algorithm", ax=ax2, palette=["blue", "green"])

plt.xlabel('Size of matrix input')
plt.title('Time and cost error of the algorithm depending on the size of the matrix')
plt.legend(loc='upper right', title="Execution time")

plt.savefig("image.png",bbox_inches='tight',dpi=100)
plt.show()