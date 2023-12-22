from genetic_algorithm import *
import matplotlib.pyplot as plt



D_DIR = "datasets/"
D_NAME = "dataset1/"
POP = 100
ITE = [50, 100, 200]
E_RATIO = 0.10
M_RATE = 0.05
results = {}
results_time = {}
for iteration in ITE:
    score_list = []
    time_list = []
    for i in range(10):
        result = genetic_algorithm(D_DIR ,D_NAME, POP, iteration, E_RATIO, M_RATE )
        computational_time = result[0]
        best_chromosome = result[1][0]
        best_score = result[1][1]
        score_list.append(best_score)
        time_list.append(computational_time)

    results[iteration] = sum(score_list)/len(score_list)
    results_time[iteration] = sum(time_list) / len(time_list)



plt.figure()
plt.plot(results.keys(), results.values(),'o-')
plt.title("Iteration size vs Objective")
plt.xlabel("Iteration size")
plt.ylabel("Objective")
plt.grid(True, linestyle='--')

plt.figure()
plt.plot(results_time.keys(), results_time.values(),'o-')
plt.title("Iteration size vs Computational time")
plt.xlabel("Iteration size")
plt.ylabel("Time(s)")
plt.grid(True, linestyle='--')
plt.show()

