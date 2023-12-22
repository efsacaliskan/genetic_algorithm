from genetic_algorithm import *
import matplotlib.pyplot as plt



D_DIR = "datasets/"
D_NAME = "dataset1/"
POP = 100
ITE = 100
E_RATIO = 0.10
M_RATE = [0, 0.025, 0.05, 0.10, 0.5]
results = {}
results_time = {}
for m in M_RATE:
    score_list = []
    time_list = []
    for i in range(10):
        result = genetic_algorithm(D_DIR ,D_NAME, POP, ITE, E_RATIO, m )
        computational_time = result[0]
        best_chromosome = result[1][0]
        best_score = result[1][1]
        score_list.append(best_score)
        time_list.append(computational_time)

    results[m] = sum(score_list)/len(score_list)
    results_time[m] = sum(time_list) / len(time_list)



plt.figure()
plt.plot(results.keys(), results.values(),'o-')
plt.title("Mutation rate vs Objective")
plt.xlabel("Mutation rate")
plt.ylabel("Objective")
plt.grid(True, linestyle='--')

plt.figure()
plt.plot(results_time.keys(), results_time.values(),'o-')
plt.title("Mutation rate vs Computational time")
plt.xlabel("Mutation rate")
plt.ylabel("Time(s)")
plt.grid(True, linestyle='--')
plt.show()

